#
# Copyright (C) 2014-2017 Red Hat, Inc.
#   This copyrighted material is made available to anyone wishing to use,
#  modify, copy, or redistribute it subject to the terms and conditions of
#  the GNU General Public License v.2.
#
#   This application is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
# Authors:
#   Guy Streeter <guy.streeter@gmail.com>
#

#
# This is just something I threw together for a Python3 ethtool.
# It shouldn't be needed, since pianofish is only being built for
# Python 2 right now.
# When there is a Python 3 ethtool port, this can go away.

'''
Copyright 2014-2017 Red Hat, Inc.
  This copyrighted material is made available to anyone wishing to use,
 modify, copy, or redistribute it subject to the terms and conditions of
 the GNU General Public License v.2.

 This application is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

Author: Guy Streeter <guy.streeter@gmail.com>
'''

import os

_basepath = '/sys/class/net'


def get_active_devices():
    nics = os.listdir(_basepath)
    names = []
    for n in nics:
        nicpath = os.path.join(_basepath, n)
        if not os.path.isdir(nicpath):
            continue
        state = ''
        with open(os.path.join(nicpath, 'operstate'), 'r') as f:
            state = f.read().strip()
        if state != 'up':
            continue
        names.append(n)
    return tuple(names)


def get_module(nic):
    nicpath = os.path.join(_basepath, nic, 'device/driver/module')
    return os.path.basename(os.path.realpath(nicpath))
