#!/usr/bin/env python

#
# Copyright (C) 2017 Red Hat, Inc.
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

from gi import require_version as gi_require_version
gi_require_version('Polkit', '1.0')

from gi.repository import Gio, GObject, Polkit, GLib

import schedutils

from pianofish import translation
from pianofish.pianofish_dbus import INTROSPECTION_XML, INTERFACE_NAME,\
    BUS_NAME, INTERFACE_ACTION, OBJECT_PATH
from pianofish.bitmap import AffinityBitmap

MAIN_LOOP = GObject.MainLoop()

def _SetIRQAffinity(irq, affinity):
    shorts = AffinityBitmap(affinity).as_shorts
    affinity_text = ','.join(['{:x}'.format(i) for i in shorts]) + '\n'
    filename = '/proc/irq/{:d}/smp_affinity'.format(irq)
    with open(filename, 'w') as f:
        f.write(affinity_text)

def handle_method_call(_connection, sender, _object_path, _interface_name,
                       method_name, parameters, invocation):
    bus_name = Polkit.SystemBusName.new(sender)
    flags = Polkit.CheckAuthorizationFlags.ALLOW_USER_INTERACTION
    result = AUTHORITY.check_authorization_sync(bus_name,
                                                INTERFACE_ACTION,
                                                None,
                                                flags)
    if not result.get_is_authorized():
        response = _('Not authorized')
        invocation.return_error_literal(Gio.dbus_error_quark(),
                                        Gio.DBusError.ACCESS_DENIED,
                                        response)
        return

    def normalize_pol_pri(pid, policy, priority):
        if policy >= 0:
            if priority == -1:
                priority = schedutils.get_priority(pid)
        elif priority >= 0:
            policy = schedutils.get_scheduler(pid)
        if policy not in (schedutils.SCHED_FIFO, schedutils.SCHED_RR):
            priority = 0
        return policy, priority

    if method_name == 'UpdateThreads':
        thread_array = parameters.unpack()[0]
        completed_pids = []
        for thread in thread_array:
            pid, policy, priority, affinity = thread
            pid = int(pid)
            policy, priority = normalize_pol_pri(pid, policy, priority)
            try:
                if policy >= 0:
                    response = _(
                        'Failed to set policy and priority for {pid}')
                    response = response.format(pid=pid)
                    schedutils.set_scheduler(pid, policy, priority)
                if affinity:
                    response = _(
                        'Failed to set affinity for {pid}')
                    response = response.format(pid=pid)
                    affinity = AffinityBitmap(affinity).schedutils_bitmasklist
                    schedutils.set_affinity(pid, affinity)
            except Exception as err:
                if completed_pids:
                    completion = _('Completed changes for PIDs: {pids}')
                    pids = ','.join(str(p) for p in completed_pids)
                    completion = completion.format(pids=pids)
                    message = _(
                        '{failure_message}\n{reason}\n\n{successes}')
                    response = message.format(failure_message=response,
                                              reason=str(err),
                                              successes=completion)
                else:
                    message = _('{failure_message}\n{reason}')
                    response = message.format(failure_message=response,
                                              reason=str(err))
                invocation.return_error_literal(Gio.dbus_error_quark(),
                                                Gio.DBusError.FAILED,
                                                response)
                return
            completed_pids.append(pid)
        invocation.return_value(GLib.Variant('(au)', (completed_pids,)))
    elif method_name == 'UpdateIRQs':
        irq_array = parameters.unpack()[0]
        completed_irqs = []
        for thread in irq_array:
            irq, pid, policy, priority, affinity = thread
            irq = int(irq)
            pid = int(pid)
            policy, priority = normalize_pol_pri(pid, policy, priority)
            try:
                if policy >= 0:
                    response = _(
                        'Failed to set policy and priority for {pid}')
                    response = response.format(pid=pid)
                    schedutils.set_scheduler(pid, policy, priority)
                if affinity:
                    response = _(
                        'Failed to set affinity for IRQ {irq}')
                    response = response.format(irq=irq)
                    _SetIRQAffinity(irq, affinity)
            except Exception as err:
                if completed_irqs:
                    completion = _('Completed changes for IRQs: {irqs}')
                    irqs = ','.join(str(p) for p in completed_irqs)
                    completion = completion.format(irqs=irqs)
                    message = _(
                        '{failure_message}\n{reason}\n\n{successes}')
                    response = message.format(failure_message=response,
                                              reason=str(err),
                                              successes=completion)
                else:
                    message = _('{failure_message}\n{reason}')
                    response = message.format(failure_message=response,
                                              reason=str(err))
                invocation.return_error_literal(Gio.dbus_error_quark(),
                                                Gio.DBusError.FAILED,
                                                response)
                return
            completed_irqs.append(irq)
        invocation.return_value(GLib.Variant('(au)', (completed_irqs,)))


def bus_acquired_handler(connection, _name):
    registration_id = connection.register_object(OBJECT_PATH,
                                                 INTERFACE_INFO,
                                                 handle_method_call,
                                                 None,
                                                 None)
    assert registration_id > 0


def name_acquired_handler(_connection, _name):
    pass


def name_lost_handler(_connection, _name):
    MAIN_LOOP.quit()

OWNER_ID = Gio.bus_own_name(Gio.BusType.SYSTEM,
                            BUS_NAME,
                            Gio.BusNameOwnerFlags.NONE,
                            bus_acquired_handler,
                            name_acquired_handler,
                            name_lost_handler)
assert OWNER_ID

INTROSPECTION_DATA = Gio.DBusNodeInfo.new_for_xml(INTROSPECTION_XML)
INTERFACE_INFO = INTROSPECTION_DATA.lookup_interface(INTERFACE_NAME)

AUTHORITY = Polkit.Authority.get_sync()


MAIN_LOOP.run()

#
