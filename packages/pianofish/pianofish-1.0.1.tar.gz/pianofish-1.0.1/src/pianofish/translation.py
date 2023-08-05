#
# Copyright (C) 2015-2017 Red Hat, Inc.
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
import os
import gettext

# for un-installed testing
try:
    __ld = os.path.dirname(__file__) + '/../locale'
    if not os.path.isdir(__ld):
        __ld = None
except:
    __ld = None

# This fake piglatin translation can be used to test that all
# displayed text is properly set up for translation. Change
# False to True, run "make translations", then run in the src
# directory with local PYTHONPATH.
if False:
    __translation = gettext.translation('pianofish', __ld,
                                        languages=['en_US@piglatin'],
                                        fallback=True)
else:
    __translation = gettext.translation('pianofish', __ld, fallback=True)

__translation.install()

del __ld
del __translation
