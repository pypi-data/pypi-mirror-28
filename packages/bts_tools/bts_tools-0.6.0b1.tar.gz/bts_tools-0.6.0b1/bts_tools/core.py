#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bts_tools - Tools to easily manage the bitshares client
# Copyright (c) 2014 Nicolas Wack <wackou@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from os.path import join, dirname, expanduser, exists, abspath
from collections import namedtuple, defaultdict, abc
from subprocess import Popen, PIPE
from functools import wraps
from jinja2 import Environment, PackageLoader
from pathlib import Path
from ruamel import yaml
import importlib
import pwd
import sys
import os
import re
import shutil
import shlex
import signal
import hashlib
import base64
import time
import logging

log = logging.getLogger(__name__)

platform = sys.platform
if platform.startswith('linux'):
    platform = 'linux'


HERE = abspath(dirname(__file__))

# FIXME: bug with supervisor in ubuntu 16.04?
# weird, seems like supervisord on ubuntu doesn't set the HOME var
# properly, even though we're running as a separate user, so do it ourself
# (otherwise, all calls to expanduser use /root for ~ and fail)
username = pwd.getpwuid(os.getuid())[0]
if os.environ.get('HOME') == '/root' and username != 'root':
    log.warning('Seems like $HOME is not properly set...')
    os.environ['HOME'] = ('/Users/{}'
                          if sys.platform == 'darwin' else
                          '/home/{}').format(username)
    log.warning('Forcing to: {}'.format(os.environ['HOME']))

BTS_TOOLS_HOMEDIR = '~/.bts_tools'
BTS_TOOLS_HOMEDIR = expanduser(BTS_TOOLS_HOMEDIR)
BTS_TOOLS_CONFIG_FILE = join(BTS_TOOLS_HOMEDIR, 'config.yaml')
BTS_TOOLS_DB_FILE = join(BTS_TOOLS_HOMEDIR, 'db.yaml')


class AttributeDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttributeDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class CaseInsensitiveAttributeDict(dict):
    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveAttributeDict, self).__init__(*args, **kwargs)
        lcase = {(k.lower(), v) for k, v in self.items()}
        self.clear()
        self.update(lcase)
        self.__dict__ = self

    def __getitem__(self, item):
        return super().__getitem__(item.lower())

    def __setitem__(self, item, value):
        return super().__setitem__(item.lower(), value)

    def __getattr__(self, item):
        return self[item.lower()]

    def __setattr__(self, key, value):
        return super().__setattr__(key, value)


config = None
db = {}
DB_VERSION = 1


def append_unique(l1, l2):
    for obj in l2:
        if obj not in l1:
            l1.append(obj)


def profile(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        plog = logging.getLogger('bts_tools.profile')

        args_str = ', '.join(str(arg) for arg in args)
        if kwargs:
            args_str + ', ' + ', '.join('%s=%s' % (k, v) for k, v in kwargs.items())

        try:
            start_time = time.time()
            result = f(*args, **kwargs)
            stop_time = time.time()
            plog.debug('Function %s(%s): returned in %0.3f ms' % (f.__name__, args_str, (stop_time-start_time)*1000))
            return result
        except Exception as e:
            stop_time = time.time()
            plog.debug('Function %s(%s): exception in %0.3f ms' % (f.__name__, args_str, (stop_time-start_time)*1000))
            plog.exception(e)
            raise e
    return wrapper


def trace(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        obj = args[0]
        args = args[1:]
        args_str = ', '.join(str(arg) for arg in args)
        if kwargs:
            args_str += ', ' + ', '.join('{}={}'.format(k, v) for k, v in kwargs)
        print('Calling function: {}({}) on {}'.format(f.__name__, args_str, obj))

        try:
            result = f(obj, *args, **kwargs)
            print('Returning {}: {}'.format(type(result).__name__, result))
        except Exception as e:
            print('Exception: {}'.format(str(e)))
            log.exception(e)
            raise e
        return result
    return wrapper


def save_db():
    global db
    log.info('Saving database file {}'.format(BTS_TOOLS_DB_FILE))
    with open(BTS_TOOLS_DB_FILE, 'w') as f:
        yaml.dump(db, f)


def load_db():
    global db

    if not config['index_full_blockchain']:
        # in this case, we'll just index what happens while the tools are online
        # this also means there's no need to persist the DB
        db = defaultdict(dict)
        db['version'] = DB_VERSION
        return

    log.info('Loading database file {}'.format(BTS_TOOLS_DB_FILE))
    try:
        with open(BTS_TOOLS_DB_FILE) as f:
            db = yaml.load(f)
        if db['version'] != DB_VERSION:
            log.info('Database version upgrade, need to reindex...')
            raise ValueError('need to reindex')
    except Exception:
        db = defaultdict(dict)
        db['version'] = DB_VERSION

    # FIXME: see http://grodola.blogspot.com/2016/02/how-to-always-execute-exit-functions-in-py.html
    import atexit
    atexit.register(save_db)


def load_config(loglevels=None):
    log.info('Using home dir for BTS tools: %s' % BTS_TOOLS_HOMEDIR)
    global config
    if not exists(BTS_TOOLS_CONFIG_FILE):
        log.info('Copying default config file to %s' % BTS_TOOLS_CONFIG_FILE)
        try:
            os.makedirs(BTS_TOOLS_HOMEDIR)
        except OSError:
            pass
        shutil.copyfile(join(dirname(__file__), 'config.yaml'),
                        BTS_TOOLS_CONFIG_FILE)

    # load config file
    try:
        log.info('Loading config file: %s' % BTS_TOOLS_CONFIG_FILE)
        config_contents = open(BTS_TOOLS_CONFIG_FILE).read()
    except:
        log.error('Could not read config file: %s' % BTS_TOOLS_CONFIG_FILE)
        raise

    env = Environment(loader=PackageLoader('bts_tools', 'templates/config'))

    # render config from template
    try:
        config_contents = env.from_string(config_contents).render()
    except:
        log.error('Could not render config file as a valid jinja2 template')
        raise

    # load yaml config
    try:
        config = yaml.load(config_contents, Loader=yaml.RoundTripLoader)
    except:
        log.error('-'*100)
        log.error('Config file contents is not a valid YAML object:')
        log.error(config_contents)
        log.error('-'*100)
        raise

    # load default config and merge
    try:
        default = env.get_template('default.yaml').render()
        default = yaml.load(default, Loader=yaml.RoundTripLoader)
    except:
        log.error('Could not load defaults for config.yaml file...')
        raise

    with open(join(BTS_TOOLS_HOMEDIR, 'default_config.yaml'), 'w') as cfg:
        cfg.write(yaml.dump(default, indent=4, Dumper=yaml.RoundTripDumper))

    def recursive_update(a, b):
        for k, v in b.items():
            if k in a:
                if isinstance(v, dict):
                    recursive_update(a[k], v)
                else:
                    a[k] = v
            else:
                a[k] = v

    recursive_update(default, config)
    config = default

    # write full_config.yaml in ~/.bts_tools
    with open(join(BTS_TOOLS_HOMEDIR, 'full_config.yaml'), 'w') as cfg:
        cfg.write(yaml.dump(config, indent=4, Dumper=yaml.RoundTripDumper))


    # setup given logging levels, otherwise from config file
    if config.get('detailed_log', False):
        # https://pymotw.com/3/cgitb/index.html
        import cgitb
        cgitb.enable(format='text')
    loglevels = loglevels or config.get('logging', {})
    for name, level in loglevels.items():
        logging.getLogger(name).setLevel(getattr(logging, level))


    # check whether config.yaml has a correct format
    m = config['monitoring']['feeds']
    if (m['bts'].get('publish_time_interval') is None and
        m['bts'].get('publish_time_slot') is None):
        log.warning('Will not be able to publish feeds. You need to specify '
                    'either publish_time_interval or publish_time_slot')

    check_time_interval = m['check_time_interval']
    publish_time_interval = m['bts'].get('publish_time_interval')
    if publish_time_interval:
        if publish_time_interval < check_time_interval:
            log.error('Feed publish time interval ({}) is smaller than check time interval ({})'.format(publish_time_interval, check_time_interval))
            log.error('Cannot compute proper period for publishing feeds...')

    # expand wildcards for monitoring plugins
    for client_name, client in config['clients'].items():
        for n in client.get('roles', []):
            n.setdefault('monitoring', [])
            if not isinstance(n['monitoring'], list):
                n['monitoring'] = [n['monitoring']]

            def add_cmdline_args(args):
                append_unique(client.setdefault('run_args', []), args)

            def add_monitoring(l2):
                append_unique(n['monitoring'], l2)

            if n['role'] == 'witness':
                # TODO: add 'prefer_backbone_exclusively' when implemented; in this case we also need:
                # TODO: "--accept-incoming-connections 0" (or limit list of allowed peers from within the client)
                add_monitoring(['missed', 'network_connections', 'voted_in', 'wallet_state', 'fork'])

            elif n['role'] == 'feed_publisher':
                add_monitoring(['feeds'])

            # options for seed node types
            elif n['role'] == 'seed':
                add_monitoring(['seed', 'network_connections', 'fork'])

            # options for backbone node types
            elif n['role'] == 'backbone':
                add_cmdline_args(['--disable-peer-advertising'])
                add_monitoring(['backbone', 'network_connections', 'fork'])

            else:
                log.warning('Unknown role: {}'.format(n['role']))

            # always check for free disk space
            add_monitoring(['free_disk_space'])

    return config


DEFAULT_BIN_FILENAMES = {'bts': ['witness_node/witness_node', 'cli_wallet/cli_wallet'],
                         'bts-testnet': ['witness_node/witness_node', 'cli_wallet/cli_wallet'],
                         'muse': ['mused/mused', 'cli_wallet/cli_wallet'],
                         'steem': ['steemd/steemd', 'cli_wallet/cli_wallet'],
                         'ppy': ['witness_node/witness_node', 'cli_wallet/cli_wallet'],
                         'ppy-testnet': ['witness_node/witness_node', 'cli_wallet/cli_wallet']
                         }

DEFAULT_GUI_BIN_FILENAMES = {'bts': '',
                             'bts-testnet': '',
                             'muse': '',
                             'steem': '',
                             'ppy': '',
                             'ppy-testnet': ''
                             }


def affiliation(type):
    """Although all supported blockchains inherit the graphene code base, they might use different versions
    and/or behaviors, and so 'affiliation' groups them in main classes of functionality.

    Currently, there are 2 main affiliations: 'bts' and 'steem'.
    """
    if type.split('-')[0] in ['bts', 'ppy']:
        return 'bts'
    elif type.split('-')[0] in ['steem', 'muse']:
        return 'steem'
    else:
        raise ValueError('No affiliation known for blockchain type: {}'.format(type))



def get_data_dir(env):
    try:
        env = config['clients'][env]
    except KeyError:
        log.error('Unknown client: %s' % env)
        sys.exit(1)

    data_dir = env.get('data_dir')
    return expanduser(data_dir) if data_dir else None


def get_gui_bin_name(build_env):
    return DEFAULT_GUI_BIN_FILENAMES.get(build_env)


def get_all_bin_names(client=None, build_env=None):
    if client is not None:
        try:
            env = config['clients'][client]
        except KeyError:
            log.error('Unknown client: %s' % client)
            sys.exit(1)

        return get_all_bin_names(build_env=env['type'])

    elif build_env is not None:
        default_names = ['witness_node/witness_node', 'cli_wallet/cli_wallet']
        if build_env not in DEFAULT_BIN_FILENAMES:
            log.warning('Using default names for binaries, might not match those for {}: {}'.format(build_env, default_names))
        return DEFAULT_BIN_FILENAMES.get(build_env, default_names)

    else:
        raise ValueError('You need to specify either a build env or a client name')


def get_full_bin_name(client=None, build_env=None):
    return get_all_bin_names(client, build_env)[0]

def get_full_cli_bin_name(client=None, build_env=None):
    return get_all_bin_names(client, build_env)[1]


def get_bin_name(client=None, build_env=None):
    return os.path.basename(get_full_bin_name(client, build_env))

def get_cli_bin_name(client=None, build_env=None):
    return os.path.basename(get_full_cli_bin_name(client, build_env))


IOStream = namedtuple('IOStream', 'status, stdout, stderr')
GlobalStatsFrame = namedtuple('GlobalStatsFrame', 'cpu_total, timestamp')
StatsFrame = namedtuple('StatsFrame', 'cpu, mem, connections, timestamp')


def quote_shell_arg(arg):
    q = shlex.quote(arg)
    if q[0] == q[-1] == "'" and '*' in q:
        # we might have shell wildcard, we want to quote using " instead of '
        q = '"{}"'.format(q[1:-1])
    return q

def join_shell_cmd(cmd):
    if isinstance(cmd, list):
        return ' '.join(quote_shell_arg(c) for c in cmd)
    elif isinstance(cmd, str):
        # we assume it's already a fully built shell string, so we shouldn't quote it twice
        #return shlex.quote(cmd)
        return cmd
    else:
        raise TypeError('Given cmd to run needs to be either a list or a str, is a {}'.format(type(cmd)))


def split_shell_cmd(cmd):
    if isinstance(cmd, str):
        return shlex.split(cmd)
    elif isinstance(cmd, list):
        return cmd
    else:
        raise TypeError('Given cmd to run needs to be either a list or a str, is a {}'.format(type(cmd)))


_SIGNAL_NAMES = dict((k, v) for v, k in signal.__dict__.items()
                     if v.startswith('SIG') and not v.startswith('SIG_'))


def _forward_signal(pid):
    def wrapped(sig, frame):
        log.debug('Forwarding signal {} ({}) to pid {}'.format(sig, _SIGNAL_NAMES.get(sig, 'UNKNOWN'), pid))
        os.kill(pid, sig)
        if sig in [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]:
            if sig == signal.SIGINT:
                log.warning('Caught Ctrl+C, exiting...')
            else:
                log.warning('Caught signal {} ({}), exiting...'.format(sig, _SIGNAL_NAMES[sig]))
            log.info('Waiting for child process to exit')
            _pid, status = os.waitpid(pid, 0)
            log.info('Child process exited with status code {}'.format(status))
            sys.exit(0)
    return wrapped


def _install_signal_forwarding(pid):
    signal.signal(signal.SIGHUP, _forward_signal(pid))
    signal.signal(signal.SIGINT, _forward_signal(pid))
    signal.signal(signal.SIGQUIT, _forward_signal(pid))
    signal.signal(signal.SIGTERM, _forward_signal(pid))
    signal.signal(signal.SIGUSR1, _forward_signal(pid))
    signal.signal(signal.SIGUSR2, _forward_signal(pid))


def _run(cmd, capture_io=False, verbose=False, run_dir=None, forward_signals=False, pidfile=None, shell=False):
    if shell:
        cmd = join_shell_cmd(cmd)
    else:
        cmd = split_shell_cmd(cmd)

    (log.info if verbose else log.debug)('SHELL: running command: %s' % join_shell_cmd(cmd))

    last_dir = os.getcwd()
    if run_dir is not None:
        log.debug('switching to run dir: {}'.format(run_dir))
        os.chdir(run_dir)

    try:
        if capture_io:
            p = Popen(cmd, shell=shell, stdout=PIPE, stderr=PIPE)
            if forward_signals:
                _install_signal_forwarding(p.pid)
            if pidfile:
                with open(expanduser(pidfile), 'w') as pidf:
                    pidf.write('{}'.format(p.pid))
            stdout, stderr = p.communicate()
            if sys.version_info[0] >= 3:
                stdout, stderr = (str(stdout, encoding='utf-8'),
                                  str(stderr, encoding='utf-8'))
            os.chdir(last_dir)  # restore previous cwd
            return IOStream(p.returncode, stdout, stderr)

        else:
            p = Popen(cmd, shell=shell)
            if forward_signals:
                _install_signal_forwarding(p.pid)
            if pidfile:
                with open(expanduser(pidfile), 'w') as pidf:
                    pidf.write('{}'.format(p.pid))
            p.communicate()
            os.chdir(last_dir)  # restore previous cwd
            return IOStream(p.returncode, None, None)

    except KeyboardInterrupt:
        log.warning('Caught Ctrl+C, exiting...')
        sys.exit(0)

    finally:
        if pidfile and os.path.exists(pidfile):
            os.remove(pidfile)


def run(cmd, capture_io=False, verbose=True, log_on_fail=True,
        run_dir=None, forward_signals=False, pidfile=None, shell=False):
    r = _run(cmd, capture_io=capture_io, verbose=verbose,
             run_dir=run_dir, forward_signals=forward_signals, pidfile=pidfile, shell=shell)
    if r.status != 0:
        if log_on_fail:
            log.warning('Failed running: %s' % cmd)
            if capture_io:
                log.warning('\nSTDOUT:\n{}\nSTDERR:\n:{}'.format(r.stdout, r.stderr))
        raise RuntimeError('Failed running: %s' % cmd)
    return r


def get_version():
    version_file = join(HERE, 'version.txt')
    if exists(version_file):
        with open(version_file) as f:
            return f.read().strip()
    try:
        return run('git describe --tags', capture_io=True, verbose=False, log_on_fail=False).stdout.strip()
    except Exception:
        return 'unknown'

VERSION = get_version()


class UnauthorizedError(Exception):
    pass


class RPCError(Exception):
    pass


class NoFeedData(Exception):
    pass


class hashabledict(dict):
    def __init__(self, *args, **kwargs):
        """try to also convert inner dicts to hashable dicts"""
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = hashabledict(v)

    def __key(self):
        return tuple(sorted(self.items()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


def make_hashable(obj):
    if isinstance(obj, (str, bytes)):
        return obj
    elif isinstance(obj, abc.Sequence):
        return tuple(make_hashable(x) for x in obj)
    elif isinstance(obj, abc.Mapping):
        return tuple((k, make_hashable(v)) for k, v in sorted(obj.items()))
    elif isinstance(obj, abc.Set):
        return frozenset(make_hashable(x) for x in obj)
    else:
        try:
            hash(obj)
        except TypeError:
            raise TypeError('make_hashable() doesn\'t know how to deal with obj type: {}, for obj {}'.format(type(obj), obj))

        return obj


def to_list(obj):
    if obj is None:
        return []
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]


def hash_salt_password(password):
    pw_bytes = password.encode('utf-8')
    salt_bytes = os.urandom(8)
    salt_b64 = base64.b64encode(salt_bytes)
    pw_hash = hashlib.sha256(pw_bytes + salt_bytes).digest()
    pw_hash_b64 = base64.b64encode(pw_hash)
    return pw_hash_b64.decode('utf-8'), salt_b64.decode('utf-8')


# FIXME: this should probably be moved somewhere else
def list_valid_plugins(plugin_type):
    """This will look for files inside a python (sub)package and return a list of names
    in this package which can be imported."""
    base_module = importlib.import_module(plugin_type)
    if 'REQUIRED_FUNCTIONS' not in dir(base_module):
        msg = 'Module {} does not look to be a valid plugins directory. It needs to define ' \
              'at least the REQUIRED_FUNCTIONS variables'.format(plugin_type)
        log.error(msg)
        return []

    base_dir = Path(base_module.__file__).parent
    result = []
    for p in base_dir.glob('*.py'):
        basename = p.parts[-1]
        if not basename.startswith('_'):
            plugin_name = basename[:-3]  # remove trailing '.py'
            # potential candidate, check for required functions
            plugin_members = dir(get_plugin(plugin_type, plugin_name))
            is_valid = True
            for func in base_module.REQUIRED_FUNCTIONS:
                if func not in plugin_members:
                    log.warning('Function {} is not defined for potential plugin {}:{}, not importing it'
                                .format(func, plugin_type, plugin_name))
                    is_valid = False
                    break
            for var in getattr(base_module, 'REQUIRED_VARS', []):  # REQUIRED_VARS is optional
                if var not in plugin_members:
                    log.warning('Variable {} is not defined for potential plugin {}:{}, not importing it'
                                .format(var, plugin_type, plugin_name))
                    is_valid = False
                    break
            if is_valid:
                result.append(plugin_name)
    return result


def get_plugin(plugin_type, plugin_name):
    plugin = importlib.import_module('{}.{}'.format(plugin_type, plugin_name))
    return plugin


def get_plugin_dict(plugin_type):
    result = CaseInsensitiveAttributeDict()
    for plugin_name in list_valid_plugins(plugin_type):
        result[plugin_name] = get_plugin(plugin_type, plugin_name)
    return result


def replace_in_file(filename, old, new, **kwargs):
    contents = open(filename).read()
    contents = re.sub(old, new, contents, **kwargs)
    open(filename, 'w').write(contents)
