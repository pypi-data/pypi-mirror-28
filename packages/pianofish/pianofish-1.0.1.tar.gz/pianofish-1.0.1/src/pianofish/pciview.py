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

from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')

from gi.repository import Gtk
import hwloc
from pianofish.utilities import Topology


class _InBitmap:
    NotIn, PartiallyCovering, ExactlyCovering, SomewhatOutside = range(4)


class _IODev(object):

    def __init__(self, hwloc_obj):
        self.hwloc_obj = hwloc_obj

    @property
    def busid(self):
        dic = {'domain': self.hwloc_obj.attr.pcidev.domain,
               'bus': self.hwloc_obj.attr.pcidev.bus,
               'dev': self.hwloc_obj.attr.pcidev.dev,
               'func': self.hwloc_obj.attr.pcidev.func,
              }
        return '{domain:04x}:{bus:02x}:{dev:02x}.{func:01x}'.format(**dic)

    def in_bitmap(self, bitmap):
        obj = self.hwloc_obj
        # find a parent obj with a cpuset
        while not obj.complete_cpuset:
            obj = obj.parent
        # Do they exactly match?
        if obj.complete_cpuset == bitmap:
            return _InBitmap.ExactlyCovering
        # Obj is at least partially covered
        if obj.complete_cpuset.intersects(bitmap):
            # ...but some slected PUs cannot reach Obj
            if not bitmap in obj.complete_cpuset:
                return _InBitmap.SomewhatOutside
            return _InBitmap.PartiallyCovering
        # None of the PUs can reach the device
        return _InBitmap.NotIn

    def description(self, _prefix):
        assert False


class _HostBridge(_IODev):

    def __init__(self, hwloc_obj):
        super(_HostBridge, self).__init__(hwloc_obj)

    def description(self, prefix):
        dic = {'busid': self.busid,
               'domain': self.hwloc_obj.attr.bridge.downstream.pci.domain,
               'secondary_bus': self.hwloc_obj.attr.bridge.downstream.pci.secondary_bus,
               'subordinate_bus': self.hwloc_obj.attr.bridge.downstream.pci.subordinate_bus,
              }
        return _('{prefix:s}{busid:s} host->PCI bridge for domain {domain:04x} bus {secondary_bus:02x}-{subordinate_bus:02x}').format(prefix=prefix, **dic)


class _PCIBridge(_IODev):

    def __init__(self, hwloc_obj):
        super(_PCIBridge, self).__init__(hwloc_obj)

    def description(self, prefix):
        dic = {'busid': self.busid,
               'vendor_id': self.hwloc_obj.attr.bridge.upstream.pci.vendor_id,
               'device_id': self.hwloc_obj.attr.bridge.upstream.pci.device_id,
               'domain': self.hwloc_obj.attr.bridge.downstream.pci.domain,
               'secondary_bus': self.hwloc_obj.attr.bridge.downstream.pci.secondary_bus,
               'subordinate_bus': self.hwloc_obj.attr.bridge.downstream.pci.subordinate_bus,
              }
        return _('{prefix:s}{busid:s} PCI->PCI bridge [{vendor_id:04x}:{device_id:04x}] for domain {domain:04x} bus {secondary_bus:02x}-{subordinate_bus:02x}').format(prefix=prefix, **dic)


class _PCIDevice(_IODev):

    def __init__(self, hwloc_obj):
        super(_PCIDevice, self).__init__(hwloc_obj)

    def description(self, prefix):
        dic = {'busid': self.busid,
               'class_id': self.hwloc_obj.attr.pcidev.class_id,
               'vendor_id': self.hwloc_obj.attr.pcidev.vendor_id,
               'device_id': self.hwloc_obj.attr.pcidev.device_id,
              }
        return _('{prefix:s}{busid:s} PCI device class {class_id:04x} vendor {vendor_id:04x} model {device_id:04x}').format(prefix=prefix, **dic)


class _OSDevice(_IODev):

    def __init__(self, hwloc_obj):
        super(_OSDevice, self).__init__(hwloc_obj)

    def description(self, prefix):
        obj = self.hwloc_obj
        while not obj.cpuset:
            obj = obj.parent
        dic = {'busid': self.busid,
               'name': self.hwloc_obj.name,
               'type': self.hwloc_obj.attr.osdev.type,
               'cpuset': str(obj.cpuset),
              }
        return _('{prefix:s}{busid:s} OS device {name:s} subtype {type:d}\n{prefix:s} on CPUs {cpuset:s}').format(prefix=prefix, **dic)


_BridgeTypes = {hwloc.OBJ_BRIDGE_HOST: _HostBridge,
                hwloc.OBJ_BRIDGE_PCI: _PCIBridge}


def _HostOrPCI(hwloc_obj):
    return _BridgeTypes[hwloc_obj.attr.bridge.upstream_type](hwloc_obj)

_DeviceTypes = {hwloc.OBJ_BRIDGE: _HostOrPCI,
                hwloc.OBJ_PCI_DEVICE: _PCIDevice,
                hwloc.OBJ_OS_DEVICE: _OSDevice,
               }


def _typeObj(hwloc_obj):
    return _DeviceTypes[hwloc_obj.type](hwloc_obj)


class PCIView(Gtk.TextView):

    def __init__(self, *args, **kwargs):
        super(PCIView, self).__init__(visible=True, editable=False,
                                      can_focus=False,
                                      wrap_mode='none', *args, **kwargs)
        buffer_ = self.get_buffer()
        selected_tag = buffer_.create_tag('selected', font='monospace 10',
                                          foreground='green')
        overflow_tag = buffer_.create_tag('overflow', font='monospace 10',
                                          foreground='orange')
        not_in_tag = buffer_.create_tag('not_in', font='monospace 10',
                                        foreground='red')
        in_tag = buffer_.create_tag('in', font='monospace 10',
                                    foreground='black')
        self._accessibility = {
            _InBitmap.NotIn : (not_in_tag, _('Unreachable')),
            _InBitmap.PartiallyCovering : (in_tag, _('Reachable')),
            _InBitmap.ExactlyCovering : (selected_tag, _('Exact')),
            _InBitmap.SomewhatOutside : (overflow_tag, _('Mismatch')),
            }
        indentation = max([len(d) for _t, d in self._accessibility.values()]) + 2
        fmt = '{:<' + str(indentation) + '}'
        for key in list(self._accessibility.keys()):
            tag, coverage = self._accessibility[key]
            coverage = fmt.format(coverage)
            self._accessibility[key] = tag, coverage
        self._padding = ' ' * indentation

    def update_selection(self, bitmap):
        buffer_ = self.get_buffer()
        start_iter, end_iter = buffer_.get_bounds()
        buffer_.delete(start_iter, end_iter)

        def walk(obj_list, prefix=''):
            for obj in obj_list:
                obj = _typeObj(obj)
                tag, descr = self._accessibility[obj.in_bitmap(bitmap)]
                buffer_.insert_with_tags(end_iter, descr, tag)
                descr = obj.description(prefix)
                descr = ('\n' + prefix + self._padding).join(descr.split('\n'))
                buffer_.insert(end_iter, descr + '\n')
                walk(obj.hwloc_obj.children, prefix + '    ')
        bridges = [b for b in Topology.bridges
                   if b.attr.bridge.upstream_type == hwloc.OBJ_BRIDGE_HOST]
        walk(bridges)
