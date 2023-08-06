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

from collections import deque
from itertools import chain, islice
from contextlib import suppress
from .feeds import check_feeds
from .core import AttributeDict
from . import core, graphene
import time
import threading
import logging

log = logging.getLogger(__name__)

# needs to be accessible at a module level (at least for now) so views can access it easily
stats_frames = {}  # dict of {rpc_key: stats_list}
global_stats_frames = []


class StableStateMonitor(object):
    """Monitor a sequence of states, and is able to compute a "stable" state value when N
    consecutive same states have happened.
    For example, we only want to decide the client is offline after 3 consecutive 'offline' states
    to absorb transient errors and avoid reacting too fast on wrong alerts.
    """
    def __init__(self, n):
        self.n = n
        self.states = deque(maxlen=n+1)
        self.last_stable_state = None

    def push(self, state):
        stable_state = self.stable_state()
        if stable_state is not None:
            self.last_stable_state = stable_state
        self.states.append(state)

    def stable_state(self):
        size = len(self.states)
        if size < self.n:
            return None
        last_state = self.states[-1]
        if all(state == last_state for state in islice(self.states, size-self.n, size)):
            return last_state
        return None

    def just_changed(self):
        stable_state = self.stable_state()
        if stable_state is None or self.last_stable_state is None:
            return False
        return stable_state != self.last_stable_state


# import all monitoring plugins
from . import monitoring


def get_config(plugin):
    return core.config['monitoring'].get(plugin, {})


def monitoring_thread(*nodes, delay=0):
    global global_stats_frames, stats_frames

    # FIXME: this should be read from config.yaml file
    # plugins acting on the client/wallet (ie: 1 instance per binary that is running)
    CLIENT_PLUGINS = ['seed', 'backbone', 'prefer_backbone_exclusively', 'network_connections',
                      'cpu_ram_usage', 'wallet_state', 'fork', 'free_disk_space']

    # plugins acting on each role (ie: 1 plugin instance for each role defined in a client)
    ROLE_PLUGINS = ['missed', 'voted_in']

    client_node = nodes[0]
    node_names = ', '.join(n.name for n in nodes)

    log.info('Starting thread monitoring on %s:%d for %s node(s): %s' %
             (client_node.wallet_host, client_node.wallet_port, client_node.type(), node_names))

    # all different types of monitoring that should be considered by this thread
    all_monitoring = set(chain(*(node.monitoring for node in nodes))) | {'cpu_ram_usage'}

    plugin_names = ', '.join(all_monitoring)
    log.info('Node(s) %s: %s: monitoring plugins loaded = %s' % (client_node.type(), node_names, plugin_names))
    # check validity of name in all_monitoring and warn for non-existent plugins
    for m in all_monitoring:
        if (m not in CLIENT_PLUGINS and
            m not in ROLE_PLUGINS and
            m not in {'feeds'}):
            log.warning('Unknown plugin specified in monitoring config: %s' % m)

    # launch async thread for communicating via websockets with a graphene witness client
    if not client_node.proxy_host:
        t = threading.Thread(target=graphene.run_monitoring, args=(client_node.type(),
                                                                   client_node.witness_host,
                                                                   client_node.witness_port,
                                                                   client_node.witness_user,
                                                                   client_node.witness_password))
        t.start()

    # launch feed monitoring and publishing thread
    if 'feeds' in all_monitoring and client_node.type().split('-')[0] in ['bts', 'steem']:
        def check_feeds_with_delay(delay=0):
            # we sleep so that all threads try to run at different times, this spreads the load better
            # and helps to have logs that are not interweaved too much
            log.debug('Waiting {} seconds before starting feeds monitoring thread for {} nodes: {}'
                      .format(delay, client_node.type(), node_names))
            time.sleep(delay)
            check_feeds(nodes)
        threading.Thread(target=check_feeds_with_delay, name='feed-thread-{}'.format(client_node.type())).start()

    # create one global context for the client, and local contexts for each node of this client
    global_ctx = AttributeDict(loop_index=0,
                               time_interval=core.config['monitoring']['monitor_time_interval'],
                               nodes=nodes)

    # FIXME: still needed?
    def init_plugin(plugin_name, node, ctx):
        try:
            init_func = getattr(monitoring, plugin_name).init_ctx
        except AttributeError:
            return  # if plugin doesn't define an init_ctx function, simply return
        try:
            init_func(node, ctx, get_config(plugin_name))
        except Exception as e:
            log.warning('While initializing context for "{}" plugin on node {}'.format(plugin_name, node))
            log.exception(e)

    for plugin_name in ['online'] + CLIENT_PLUGINS:
        init_plugin(plugin_name, client_node, global_ctx)

    # note: we can use node.name as a key here, as they are all from a same client. However
    #       it is to be noted that 2 nodes with the same name (eg: witness monitoring and
    #       feed publisher) will share the same context
    contexts = {}
    for node in nodes:
        ctx = contexts.get(node.name, AttributeDict())
        for plugin_name in ROLE_PLUGINS:
            init_plugin(plugin_name, node, ctx)

        contexts[node.name] = ctx

    # reindex the db if any plugin notified us to do so
    static_values = core.db[client_node.rpc_id].get('static', {})
    if static_values.get('need_reindex'):
        static_values['need_reindex'] = False
        core.db[client_node.rpc_id] = {'static': static_values}
    monitoring.indexing.init_ctx(client_node, global_ctx, get_config(plugin_name))

    # make the stats values available to the outside
    stats_frames[client_node.rpc_id] = global_ctx.stats
    if monitoring.cpu_ram_usage.cpu_total_ctx == global_ctx:
        global_stats_frames = global_ctx.global_stats

    # we sleep so that all threads try to run at different times, this spreads the load better
    # and helps to have logs that are not interweaved too much
    log.debug('Waiting {} seconds before starting monitoring thread for {} nodes: {}'.format(delay, client_node.type(), node_names))
    time.sleep(delay)

    while True:
        global_ctx.loop_index += 1

        # log.debug('-------- Monitoring status of the BitShares client --------')
        client_node.clear_rpc_cache()

        try:
            online = monitoring.online.monitor(client_node, global_ctx, get_config('online'))
            if not online:
                # we still want to monitor global cpu usage when client is offline
                monitoring.cpu_ram_usage.monitor(client_node, global_ctx, get_config('cpu_ram_usage'))

                time.sleep(global_ctx.time_interval)  # sleep here before looping again
                continue

            # start by indexing new blocks for given client
            if monitoring.indexing.is_valid_node(client_node):
                monitoring.indexing.monitor(client_node, global_ctx, get_config(plugin_name))

            # monitor at a client level
            global_ctx.info = client_node.info()
            for plugin_name in CLIENT_PLUGINS:
                if plugin_name in all_monitoring:
                    try:
                        plugin = getattr(monitoring, plugin_name)
                        if plugin.is_valid_node(client_node):
                            plugin.monitor(client_node, global_ctx, get_config(plugin_name))
                    except Exception as e:
                        log.error('An exception happened in monitoring plugin: %s' % plugin_name)
                        log.exception(e)

            # monitor each node/role individually
            for node in nodes:
                ctx = contexts[node.name]
                ctx.info = global_ctx.info
                ctx.online_state = global_ctx.online_state
                for plugin_name in ROLE_PLUGINS:
                    if plugin_name in node.monitoring:
                        try:
                            plugin = getattr(monitoring, plugin_name)
                            if plugin.is_valid_node(node):
                                plugin.monitor(node, ctx, get_config(plugin_name))
                        except Exception as e:
                            log.error('An exception happened in monitoring plugin: %s' % plugin_name)
                            log.exception(e)

        except Exception as e:
            log.error('An exception occurred in the monitoring thread:')
            log.exception(e)

        time.sleep(global_ctx.time_interval)
