#!/usr/bin/env python

#
# Copyright (C) 2016-2017 Red Hat, Inc.
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

from __future__ import print_function

OBJECT_PATH = '/org/fedora/pianofish1'

# The bus name is what the server advertises and the client requests,
# to initially connect to each other. The org.fedora.pianofish.service
# file tells DBus where to find and start the server if it isn't running.
# for that to work, we would need to install the pianofish-server.py file
# in the specified location.
BUS_NAME = 'org.fedora.pianofish1'

# This matches the interface name in our introspection XML data. The
# server could support multiple interfaces. It would probably be more
# clear if we used text that was different from the bus name.
INTERFACE_NAME = 'org.fedora.pianofish1'

# This is the action we request polkit to authorize us for. It is
# specified in the pianofish.policy file, installed in the polkit policy
# directory
INTERFACE_ACTION = 'org.fedora.pianofish1.admin'

INTROSPECTION_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
  "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">

<node name="/org/fedora/pianofish1">
  <interface name="org.fedora.pianofish1">

    <!--
      UpdateThreads:
      @changes: Array of (pid, policy, priority, affinity) to change.
      @successes: Returned array of PIDs successfully changed.

      Set the scheduling policy, realtime priority, and CPU affinity for
      each PID.
      policy or priority -1 will be unchanged. If the new policy is not a
      realtime policy, priority will be ignored.
      affinity is a string representation (e.g. "1-3,5"). An empty string
      will be unchanged.
      If there are any errors, error reply will be returned instead of
      method reply.
    -->
    <method name="UpdateThreads">
      <arg name="changes" type="a(uiis)" direction="in" />
      <arg name="successes" type="au" direction="out" />
    </method>

    <!--
      UpdateIRQs:
      @changes: Array of (IRQ, PID, policy, priority, affinity) to change.
      @successes: Returned array of IRQs successfully changed.

      Set the sCPU affinity of each IRQ, and the cheduling policy and
      realtime priority of the associated PID.
      policy or priority -1 will be unchanged. If the new policy is not a
      realtime policy, priority will be ignored.
      affinity is a string representation (e.g. "1-3,5"). An empty string
      will be unchanged.
      If there are any errors, error reply will be returned instead of
      method reply.
    -->
    <method name="UpdateIRQs">
      <arg name="changes" type="a(uuiis)" direction="in" />
      <arg name="successes" type="au" direction="out" />
    </method>
  </interface>
</node>
"""

if __name__ == '__main__':
    filename = 'pianofish1_dbus.xml'
    with open(filename, 'w') as xml_out:
        xml_out.write(INTROSPECTION_XML)
    print('wrote introspection data to "%s"' % (filename,))
