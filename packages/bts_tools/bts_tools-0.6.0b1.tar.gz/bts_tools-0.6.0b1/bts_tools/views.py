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

from flask import Blueprint, Response, render_template, request, redirect, send_from_directory, jsonify
from functools import wraps
from collections import defaultdict
from datetime import datetime
from . import rpcutils as rpc
from . import core, monitor, slogging, backbone, seednodes, network_utils, feeds
from .seednodes import split_columns
import bts_tools
import psutil
import json
import requests.exceptions
import logging

log = logging.getLogger(__name__)

bp = Blueprint('web', __name__, static_folder='static', template_folder='templates')


@bp.route('/robots.txt')
#@bp.route('/sitemap.xml')
def static_from_root():
    """Allows to serve static files directly from the root url instead of the
    static folder. Files still need to be put inside the static folder."""
    return send_from_directory(bp.static_folder, request.path[1:])


@core.profile
def offline():
    try:
        build_env_name = rpc.main_node.client()['type']
        client_name = core.get_gui_bin_name(build_env_name)
    except:
        client_name = 'Graphene (unidentified)'

    return render_template('error.html',
                           msg='The %s cli wallet is currently offline. '
                               'Please run it and activate the HTTP RPC server.'
                               % client_name)


@core.profile
def unauthorized():
    return render_template('error.html',
                           msg=('Unauthorized. Make sure you have correctly set '
                                'the rpc user and password in the %s file'
                                % core.BTS_TOOLS_CONFIG_FILE))


@core.profile
def server_error(msg='An unknown server error occurred... Please check your log files.'):
    return render_template('error.html', msg=msg)


def catch_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            core.is_online = False
            return offline()
        except core.RPCError as e:
            if 'Connection aborted' in str(e):
                core.is_online = False
                return offline()
            elif 'fund != nullptr: Invalid reward fund name' in str(e):
                # trying to access the reward fund via the cli_wallet, but it still doesn't exist...
                return server_error('Cannot access reward fund from the witness client as it is still syncing. '
                                    'Please wait until it has synced at least up to HF17')
            else:
                log.error('While processing %s()' % f.__name__)
                log.exception(e)
                return server_error()
        except core.UnauthorizedError:
            return unauthorized()
        except Exception as e:
            log.error('While processing %s()' % f.__name__)
            log.exception(e)
            return server_error()
    return wrapper


# Note: before each view, we clear the rpc cache, and have cached=True by default
# this allows to ensure we only perform a given rpc call once with a given set
# of args, no matter how many times we call it from the view (ie: we might need
# to call 'is_online' or 'info' quite a few times, and we don't want to be sending
# all these requests over ssh...)
def clear_rpc_cache(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        rpc.main_node.clear_rpc_cache()
        return f(*args, **kwargs)
    return wrapper


@bp.route('/')
def homepage():
    return redirect('/info')


@bp.route('/status')
@clear_rpc_cache
@catch_error
@core.profile
def view_status():
    #log.debug('getting stats from: %s' % hex(id(monitor.stats)))

    # note: in uWSGI, without lazy-apps=true, monitor.stats seems to not be
    #       properly shared and always returns an empty deque...
    #log.debug('stats size: %d' % len(monitor.stats))
    if rpc.main_node.status() == 'unauthorized':
        return unauthorized()

    stats = list(monitor.stats_frames.get(rpc.main_node.rpc_id, []))

    points = [(int((stat.timestamp - datetime(1970,1,1)).total_seconds() * 1000),
               stat.cpu,
               int(stat.mem / (1024*1024)),
               stat.connections)
              for stat in stats]

    gpoints = [(int((stat.timestamp - datetime(1970,1,1)).total_seconds() * 1000),
                stat.cpu_total)
               for stat in list(monitor.global_stats_frames)]

    total_ram = None  # total RAM in MB
    if rpc.main_node.is_localhost():
        total_ram = psutil.virtual_memory().total / (1024*1024)

    return render_template('status.html', title='BTS Client - Status', points=points, gpoints=gpoints, total_ram=total_ram)


def find_node(type, host, name):
    for node in rpc.nodes:
        if node.type() == type and '{}:{}'.format(node.wallet_host, node.wallet_port) == host and node.name == name:
            return node
    raise ValueError('Node not found: {}/{}/{}'.format(type, host, name))


def find_local_node(port):
    for node in rpc.nodes:
        if node.is_localhost() and node.wallet_port == port:
            return node
    raise ValueError('Node not found: localhost:{}'.format(port))


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        log.debug('Authentication: {}'.format(auth))
        #if not auth or not check_auth(auth.username, auth.password):
        #    return authenticate()
        return f(*args, **kwargs)
    return wrapper


# FIXME: get auth params (user, password) like this: http://flask.pocoo.org/snippets/8/
#        instead of passing them as additional params
#        we also need to make sure that nginx forwards the auth params to the flask app
@bp.route('/rpc', methods=['POST'])
@requires_auth
def json_rpc_call():
    try:
        c = json.loads(next(request.form.keys()))
    except StopIteration:
        c = json.loads(request.data.decode('utf-8'))

    log.debug('json rpc call: {}'.format(c))

    method, params = c['params'][1], c['params'][2]  # NOTE: this works only for graphene clients
    port = c.pop('wallet_port', None)
    proxy_user = c.pop('proxy_user', '')
    proxy_password = c.pop('proxy_password', '')
    # FIXME SECURITY: check credentials before forwarding call to cli wallet

    try:
        node = find_local_node(port)
        user = node.wallet_user
        password = node.wallet_password

        # Intercept api calls meant for the bts_tools and do not forward them to the cli wallet
        if method in ['is_signing_key_active', 'network_get_info', 'network_get_connected_peers',
                        'network_get_potential_peers', 'network_get_advanced_parameters',
                        'network_set_advanced_parameters']:

            result = {'result': getattr(node, method)(*params)}
        else:
            result = rpc.rpc_call('localhost', port, user, password, method, *params,
                                  __graphene=True, raw_response=True)

        result['id'] = c['id']  # need to set back the original request id

    except ValueError as e:
        result = {'id': c['id'], 'error': {'message': 'Could not find active node on port {}'.format(port)}}

    except core.RPCError as e:
        result = {'id': c['id'], 'error': {'message': str(e)}}

    return jsonify(result)


@bp.route('/info')
@clear_rpc_cache
@catch_error
@core.profile
def view_info():
    attrs = defaultdict(list)
    n = rpc.main_node
    try:
        info = n.info()
    except Exception as e:
        log.exception(e)
        info = {}
    # TODO: we should cache the witness and committee member names, they never change
    info['active_witnesses'] = n.get_active_witnesses()
    if n.type() in ['bts', 'bts-testnet']:
        info['active_committee_members'] = [n.get_committee_member_name(cm)
                                            for cm in info['active_committee_members']]
    info_items = sorted(info.items())

    attrs['bold'] = [(i, 0) for i in range(len(info_items))]
    for i, (prop, value) in enumerate(info_items):
        def green_if_true(cond):
            if cond:
                attrs['green'].append((i, 1))
            else:
                attrs['red'].append((i, 1))

        if prop in {'wallet_open',
                    'wallet_unlocked',
                    'wallet_block_production_enabled'}:
            if rpc.main_node.is_witness():
                green_if_true(value)

        elif prop == 'network_num_connections':
            green_if_true(value >= 5)

        elif prop == 'blockchain_head_block_age':
            green_if_true(value is not None and value < 60)

        elif prop == 'blockchain_average_delegate_participation':
            value = float(value)
            if value < 90:
                attrs['orange'].append((i, 1))
            elif value < 80:
                attrs['red'].append((i, 1))

        elif prop == 'wallet_next_block_production_time':
            if value and value < 60:
                attrs['orange'].append((i, 1))

        elif prop in {'blockchain_head_block_timestamp',
                      'blockchain_next_round_timestamp',
                      'ntp_time',
                      'wallet_last_scanned_block_timestamp',
                      'wallet_next_block_production_timestamp',
                      'wallet_unlocked_until_timestamp'}:
            if value is not None:
                attrs['datetime'].append((i, 1))

    #if not rpc.main_node.is_graphene_based():
    #    info_items, attrs = split_columns(info_items, attrs)

    global feeds
    feeds_obj = {}

    if rpc.main_node.is_witness() and rpc.main_node.type() in ['bts']:
        published_feeds = rpc.main_node.get_witness_feeds(rpc.main_node.name, feeds.visible_feeds)
        if len(published_feeds) > 0:
            last_update = max(f.last_updated for f in published_feeds) if published_feeds else None
            pfeeds = {f.asset: f.price for f in published_feeds}
            bfeeds = {f.asset: f.price for f in rpc.main_node.get_blockchain_feeds(feeds.visible_feeds)}
            lfeeds = dict(feeds.feeds)
            mfeeds = {cur: feeds.median_str(cur) for cur in lfeeds}

            # format to string here instead of in template, more flexibility in python
            def format_feeds(fds):
                for asset in feeds.visible_feeds:
                    fmt, field_size = (('%.4g', 10)
                                      if feeds.is_extended_precision(asset)
                                      else ('%.4f', 7))
                    try:
                        s = fmt % float(fds[asset])
                    except:
                        s = 'N/A'
                    fds[asset] = s.rjust(field_size)

            format_feeds(lfeeds)
            format_feeds(mfeeds)
            format_feeds(pfeeds)
            format_feeds(bfeeds)

            feeds_obj = dict(assets=feeds.visible_feeds, feeds=lfeeds, pfeeds=pfeeds,
                            mfeeds=mfeeds, bfeeds=bfeeds, last_update=last_update)

    if rpc.main_node.is_witness():
        info_items2 = sorted(rpc.main_node.get_witness(rpc.main_node.name).items())
        attrs2 = defaultdict(list)
        attrs2['bold'] = [(i, 0) for i in range(len(info_items))]
    else:
        info_items2 = None
        attrs2 = None

    return render_template('info.html', #title='BTS Client - Info',
                           title='Global info', data=info_items, attrs=attrs,
                           title2='Witness info', data2=info_items2, attrs2=attrs2,
                           **feeds_obj)


@bp.route('/rpchost/<type>/<host>/<name>/<url>')
@catch_error
def set_rpchost(type, host, name, url):
    try:
        rpc.main_node = find_node(type, host, name)
        log.debug('Setting main rpc node to %s %s on %s' % (type, name, host))
    except ValueError:
        # invalid host name
        log.debug('Invalid node name: %s on %s' % (name, host))
        pass

    return redirect(url)


@bp.route('/witness/<witness_name>')
@clear_rpc_cache
@catch_error
@core.profile
def view_witness(witness_name):
    attrs = defaultdict(list)
    info_items = sorted(rpc.main_node.get_witness(witness_name).items())

    attrs['bold'] = [(i, 0) for i in range(len(info_items))]

    return render_template('tableview.html',
                           data=info_items, attrs=attrs)


@bp.route('/witnesses')
@clear_rpc_cache
@catch_error
@core.profile
def view_delegates():
    # FIXME: deprecate?
    return redirect('https://bitshares.openledger.info/#/explorer/witnesses')


@bp.route('/backbone')
@clear_rpc_cache
@catch_error
@core.profile
def view_backbone_nodes():
    backbone_nodes = backbone.node_list(rpc.main_node)
    if not backbone_nodes:
        return render_template('error.html',
                       msg='No backbone nodes currently configured in the config.yaml file...')

    peers = rpc.main_node.network_get_connected_peers()

    headers = ['Address', 'Status', 'Connected since', 'Platform', 'BitShares git time', 'fc git time']

    attrs = defaultdict(list)
    for i, _ in enumerate(peers):
        attrs['datetime'].append((i, 2))
        attrs['datetime'].append((i, 4))
        attrs['datetime'].append((i, 5))

    connected = {}
    for p in peers:
        if p['addr'] in backbone_nodes:
            connected[p['addr']] = p

    data = [(connected[p]['addr'],
             '<div class="btn btn-xs btn-success">online</div>',
             connected[p]['conntime'],
             connected[p].get('platform'),
             connected[p].get('bitshares_git_revision_unix_timestamp', 'unknown'),
             connected[p].get('fc_git_revision_unix_timestamp', 'unknown'))
             if p in connected else
             (p,
              '<div class="btn btn-xs btn-danger">offline</div>',
              '', '', '', '')
             for p in backbone_nodes ]

    return render_template('network.html',
                           title='Backbone nodes',
                           headers=headers,
                           data=data, attrs=attrs, order='[[ 1, "desc" ]]')


@bp.route('/network/<chain>/seednodes')
@clear_rpc_cache
@catch_error
@core.profile
def view_seed_nodes(chain):
    headers = ['seed host', 'status'] * 2
    data = seednodes.get_seeds_view_data(chain)
    headers *= (len(data[0]) // len(headers))

    return render_template('tableview.html',
                           title='{} seed nodes'.format(chain),
                           headers=headers,
                           data=data, order='[]', nrows=100, sortable=False)





@bp.route('/peers')
@clear_rpc_cache
@catch_error
@core.profile
def view_connected_peers():
    try:
        peers = rpc.main_node.network_get_connected_peers()
    except KeyError:
        raise requests.exceptions.ConnectionError  # (ab)use this to set the status to offline

    headers = ['Address', 'Connected since', 'Platform', 'BitShares git time', 'fc git time']

    attrs = defaultdict(list)
    for i, _ in enumerate(peers):
        attrs['datetime'].append((i, 1))
        attrs['datetime'].append((i, 3))
        attrs['datetime'].append((i, 4))

    data = [ (p['addr'],
              p['conntime'],
              p.get('platform'),
              p.get('bitshares_git_revision_unix_timestamp', 'unknown'),
              p.get('fc_git_revision_unix_timestamp', 'unknown'))
             for p in peers ]

    countries = defaultdict(int)

    points = network_utils.get_world_map_points_from_peers(peers)

    for pt in points:
        countries[pt['country_iso'].lower()] += 1

    #print(json.dumps(countries, indent=4))

    return render_template('network_map.html',
                           title='Connected peers',
                           headers=headers,
                           points=points,
                           countries=countries,
                           data=data, attrs=attrs, order='[[ 1, "desc" ]]')


@bp.route('/peers/potential')
@clear_rpc_cache
@catch_error
@core.profile
def view_potential_peers():
    try:
        peers = rpc.main_node.network_get_potential_peers()
    except KeyError:
        raise requests.exceptions.ConnectionError  # (ab)use this to set the status to offline

    # TODO: find a better way to do this, see https://github.com/BitShares/bitshares/issues/908
    peers = peers[:300]

    headers = ['Address', 'Last connection time', 'Last connection status', 'Last seen',
               'Successful connections', 'Failed connections']

    attrs = defaultdict(list)
    for i in range(len(peers)):
        attrs['datetime'].append((i, 1))
        attrs['datetime'].append((i, 3))

    def fmt(conn_status):
        lc = 'last_connection_'
        return conn_status[len(lc):] if conn_status.startswith(lc) else conn_status

    data = [ (p['endpoint'],
              p['last_connection_attempt_time'],
              fmt(p['last_connection_disposition']),
              p['last_seen_time'],
              p['number_of_successful_connection_attempts'],
              p['number_of_failed_connection_attempts'])
             for p in peers ]

    return render_template('network.html',
                           title='Potential peers',
                           headers=headers,
                           data=data, attrs=attrs, order='[[ 1, "desc" ]]')


@bp.route('/logs')
@clear_rpc_cache
@catch_error
@core.profile
def view_logs():
    records = list(slogging.log_records)

    headers = ['Timestamp', 'Level', 'Logger', 'Message']

    data = [(r.asctime,
             r.levelname,
             '%s:%s %s' % (r.name, r.lineno, r.funcName),
             r.msg)
            for r in reversed(records)]

    attrs = defaultdict(list)
    for i, d in enumerate(data):
        color = None
        if d[1] == 'INFO':
            color = 'green'
        elif d[1] == 'DEBUG':
            color = 'blue'
        elif d[1] == 'WARNING':
            color = 'orange'
        elif d[1] == 'ERROR':
            color = 'red'

        if color:
            attrs[color].extend([(i, 1), (i, 2)])

    return render_template('tableview.html',
                           headers=headers,
                           data=data,
                           attrs=attrs,
                           order='[]')
