#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bts_tools - Tools to easily manage the bitshares client
# Copyright (c) 2017 Nicolas Wack <wackou@gmail.com>
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

from ..core import run, replace_in_file
from pathlib import Path
import os
import psutil
import logging

log = logging.getLogger(__name__)


def short_description():
    return 'download, compile and install the specified boost version'


def help():
    return """truncate <block_num>
    
block_num: number of blocks to keep in blockchain
"""


# FIXME: implement me properly

def run_command(boost_ver=60, base_build_dir=None, prefix=None):
    # note: do not use default args in the function definition as os.environ['HOME'] is
    #       not defined when running from a non-shell session (eg: supervisord) and it
    #       makes the file un-importable
    base_build_dir = Path(base_build_dir or os.environ['HOME']).expanduser()
    prefix = Path(prefix or os.environ['HOME']).expanduser()

    log.info('Downloading boost version 1.{} into: {}'.format(boost_ver, base_build_dir))
    os.chdir(str(base_build_dir))
    if not Path('boost_1_{}_0.tar.gz'.format(boost_ver)).exists():
        run('wget http://downloads.sourceforge.net/project/boost/boost/1.{boost_ver}.0/boost_1_{boost_ver}_0.tar.gz'
            .format(boost_ver=boost_ver))
    else:
        log.info('Not downloading it, file is already present')

    log.info('Decompressing source tarball')
    run('tar xf boost_1_{}_0.tar.gz'.format(boost_ver))
    os.chdir('boost_1_{}_0'.format(boost_ver))

    if boost_ver == 60:
        log.info('Applying patch for boost 1.60')
        replace_in_file('boost/multiprecision/cpp_int.hpp',
                        r'BOOST_STATIC_CONSTANT(limb_type, sign_bit_mask = 1u << (limb_bits - 1))',
                        r'BOOST_STATIC_CONSTANT(limb_type, sign_bit_mask = static_cast<limb_type>(1u) << (limb_bits - 1))')

    log.info('Bootstrapping install')
    run('./bootstrap.sh')

    log.info('Compiling and installing')
    run('./b2 --without-python -j{} --prefix={}/boost_1.{}_install install'.format(psutil.cpu_count(), prefix, boost_ver))

