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
#   Guy Streeter <guy.streeter@gmail.com> <guy.streeter@gmail.com>
#

import hwloc


class AffinityBitmap(hwloc.Bitmap):

    """AffinityBitmap(reference)
    reference can be a Bitmap, a list of bit numbers, a selection string,
    or None"""

    ArgError = hwloc.ArgError

    def __init__(self, reference=None):
        if isinstance(reference, hwloc.Bitmap):
            super(AffinityBitmap, self).__init__(reference)
            return
        super(AffinityBitmap, self).__init__()
        if reference is None:
            return
        if isinstance(reference, str):
            self.set_from_text(reference)
        else:
            self.set_from_list(reference)

    def set_from_list(self, bit_list):
        self.zero()
        for bit in bit_list:
            self.set(bit)

    def set_from_text(self, text):
        if '0x' in text:
            self.sscanf(text)
        else:
            self.list_sscanf(text)

    def get_friendly_text(self, list_max=24):
        text = self.list_asprintf()
        if len(text) > list_max:
            return str(self)
        return text

    @property
    def schedutils_bitmasklist(self):
        # schedutils insists on a list, not a tuple?
        return list(self.all_set_bits)

    @property
    def as_shorts(self):
        return tuple([int(text, 16) for text in str(self).split(',')])
