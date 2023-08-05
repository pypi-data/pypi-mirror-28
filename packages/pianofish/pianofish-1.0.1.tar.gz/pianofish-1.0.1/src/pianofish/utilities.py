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
gi_require_version('Polkit', '1.0')
gi_require_version('Pango', '1.0')
gi_require_version('PangoCairo', '1.0')

# some versions need Pango imported before Gtk
from gi.repository import Pango
from gi.repository import Gtk, GObject, GLib, Polkit, Gio, Gdk, PangoCairo

import cairo
import re
import threading
import time

import hwloc
import procfs
import schedutils
import ethtool

from pianofish.bitmap import AffinityBitmap
from pianofish.pianofish_dbus import INTERFACE_ACTION, BUS_NAME,\
    OBJECT_PATH, INTERFACE_NAME


def set_text_drag_icon(widget, context, text):
    pango_layout = widget.create_pango_layout(text)
    width, height = pango_layout.get_pixel_size()
    window = widget.get_window()
    surface = window.create_similar_surface(cairo.CONTENT_ALPHA,
                                            width, height)
    cairo_context = cairo.Context(surface)
    PangoCairo.show_layout(cairo_context, pango_layout)
    pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)
    Gtk.drag_set_icon_pixbuf(context, pixbuf, width, height)


class Signaler(GObject.Object):

    def __init__(self, signal_name):
        super(Signaler, self).__init__()
        self._signal_name = signal_name
        GObject.signal_new(self._signal_name, Signaler,
                           GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                           ())

    def connect_handler(self, handler):
        self.connect(self._signal_name, handler)

    def emit_signal(self):
        self.emit(self._signal_name)

class RowItem(object):

    def __init__(self, title, keyword, type_, attributes=None, cell_props=None):
        self._title = title
        self._keyword = keyword
        self._type = type_
        self._attributes = attributes if attributes else []
        self._cell_props = cell_props if cell_props else []

    @property
    def type(self):
        return self._type

    @property
    def keyword(self):
        return self._keyword

    @property
    def attributes(self):
        return self._attributes

    @property
    def cell_props(self):
        return self._cell_props

    def __str__(self):
        return self._title


class TextRow(object):
    def __init__(self, columns):
        self.columns = columns
        self.nr_columns = len(columns)
        self._reverse_dict = {}
        cols = []
        for col_num, col in enumerate(columns):
            self._reverse_dict[col.keyword] = col_num
            cell_renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col, cell_renderer, text=col_num)
            column.set_sort_column_id(col_num)
            column.set_reorderable(True)
            column.set_resizable(True)
            for attr, value in col.attributes:
                column.set_property(attr, value)
            for prop, value in col.cell_props:
                cell_renderer.set_property(prop, value)
            cols.append(column)
        self.treeview_columns = tuple(cols)

    def __getitem__(self, keywd):
        return self._reverse_dict[keywd]

    def listview_columns(self):
        for col in self.columns:
            yield col.type


class TextListStore(Gtk.ListStore):
    def __init__(self, row, **kwargs):
        coltypes = row.listview_columns()
        super(TextListStore, self).__init__(*coltypes, **kwargs)
        self.set_sort_column_id(row.sort_column, Gtk.SortType.ASCENDING)

    def set_row_values(self, row, values):
        self.set(row, dict(enumerate(values)))


class TextTreeStore(Gtk.TreeStore):
    def __init__(self, row, **kwargs):
        coltypes = row.listview_columns()
        super(TextTreeStore, self).__init__(*coltypes, **kwargs)
        self.set_sort_column_id(row.sort_column, Gtk.SortType.ASCENDING)

    def set_row_values(self, row, values):
        self.set(row, dict(enumerate(values)))


class TextTreeView(Gtk.TreeView):
    def __init__(self, row, *args, **kwargs):
        super(TextTreeView, self).__init__(rules_hint=True, *args, **kwargs)
        for column in row.treeview_columns:
            self.append_column(column)


class WeightedTextRow(object):
    def __init__(self, columns):
        self.columns = columns
        self.nr_columns = len(columns)
        self._reverse_dict = {}
        cell_renderer = Gtk.CellRendererText()
        cols = []
        for col_num, col in enumerate(self.columns):
            self._reverse_dict[col.keyword] = col_num
            column = Gtk.TreeViewColumn(col, cell_renderer, text=col_num)
            column.set_sort_column_id(col_num)
            column.set_reorderable(True)
            column.set_resizable(True)
            column.add_attribute(cell_renderer, 'weight',
                                 col_num + self.nr_columns)
            for prop, value in col.cell_props:
                cell_renderer.set_property(prop, value)
            for prop, value in col.attributes:
                column.set_property(prop, value)
            cols.append(column)
        self.treeview_columns = tuple(cols)

    def __getitem__(self, keywd):
        return self._reverse_dict[keywd]

    def listview_columns(self):
        for col in self.columns:
            yield col.type
        for _ in range(self.nr_columns):
            yield int


class WeightedTextListStore(TextListStore):

    def __init__(self, row, **kwargs):
        super(WeightedTextListStore, self).__init__(row, **kwargs)

    def set_row_values(self, row, values):
        weights = []
        for column, value in enumerate(values):
            if self.get_value(row, column) == value:
                weight = Pango.Weight.NORMAL
            else:
                weight = Pango.Weight.BOLD
            weights.append(weight)
        self.set(row, tuple(range(len(values) * 2)),
                 tuple(values) + tuple(weights))


class WeightedTextTreeStore(TextTreeStore):

    def __init__(self, row, **kwargs):
        super(WeightedTextTreeStore, self).__init__(row, **kwargs)

    def set_row_values(self, row, values):
        weights = []
        for column, value in enumerate(values):
            if self.get_value(row, column) == value:
                weight = Pango.Weight.NORMAL
            else:
                weight = Pango.Weight.BOLD
            weights.append(weight)
        self.set(row, tuple(range(len(values) * 2)),
                 tuple(values) + tuple(weights))


class WeightedTextTreeView(TextTreeView):

    def __init__(self, row, *args, **kwargs):
        super(WeightedTextTreeView, self).__init__(row, *args,
                                                   enable_tree_lines=True,
                                                   enable_grid_lines=True,
                                                   **kwargs)


class PolicyChooser(Gtk.Grid):
    unchanged_text = _('<Unchanged>')

    def __init__(self, policy=None, *args, **kwargs):
        super(PolicyChooser, self).__init__(visible=True,
                                            orientation='vertical',
                                            row_homogeneous=False,
                                            *args, **kwargs)
        sched_policies = (schedutils.SCHED_OTHER,
                          schedutils.SCHED_FIFO,
                          schedutils.SCHED_RR,
                          schedutils.SCHED_BATCH,
                          schedutils.SCHED_IDLE)
        self._check_button = Gtk.CheckButton(visible=True, halign='start',
                                             label=_('_Policy'),
                                             use_underline=True)
        self._check_button.set_active(False)
        self.add(self._check_button)
        self._combo_box = Gtk.ComboBoxText(visible=True, has_frame=False,
                                           halign='fill')
        self._check_button.get_child().set_mnemonic_widget(self._combo_box)
        self._original_policy = policy
        self._policy = policy
        if policy:
            for pol in sched_policies:
                polstr = schedutils.schedstr(pol).replace('SCHED_', '')
                self._combo_box.append(polstr, polstr)
            if policy == self.unchanged_text:
                self._combo_box.append(policy, policy)
            self.selected_policy = policy
            self._combo_box.set_active_id(policy)
            self._combo_box.connect('changed', self._on_combo_box_changed)
        else:
            self._combo_box.append_text('<none>')
            self._combo_box.set_sensitive(False)
        self.add(self._combo_box)

    def _on_combo_box_changed(self, widget):
        # in case we want to be notified on a change
        self.selected_policy = self._combo_box.get_active_id()
        changed = self.selected_policy != self._original_policy
        self._check_button.set_active(changed)

    @GObject.property(str, '')
    def selected_policy(self):
        return 'SCHED_' + self._policy

    @selected_policy.setter
    def selected_policy(self, value):
        self._policy = value

    @property
    def unchanged(self):
        return not self._check_button.get_active()


class PriorityChooser(Gtk.Grid):
    unchanged_text = _('<Unchanged>')

    def __init__(self, priority, pmin=1, pmax=99, *args, **kwargs):
        super(PriorityChooser, self).__init__(visible=True,
                                              orientation='vertical',
                                              row_homogeneous=False,
                                              *args, **kwargs)
        self._priority = priority
        self._check_button = Gtk.CheckButton(visible=True, halign='start',
                                             label=_('_Scheduler Priority'),
                                             use_underline=True,)
        self.add(self._check_button)
        self._spin_button = Gtk.SpinButton(visible=True, numeric=False,
                                           expand=True, climb_rate=1,
                                           halign='fill')
        self._spin_button.connect('value-changed', self._on_value_changed)
        self._check_button.get_child().set_mnemonic_widget(self._spin_button)
        self._original_priority = priority
        if priority is not None:
            set_priority = 1 if priority == self.unchanged_text\
                else priority
            adj = Gtk.Adjustment(set_priority, pmin, pmax, 1, 10, 0)
            self._spin_button.set_adjustment(adj)
            self._check_button.set_active(False)
            if priority == self.unchanged_text:
                self._spin_button.set_value(1.0)
                self._original_priority = -1
            self._spin_button.set_value(set_priority)
            self._spin_button.bind_property('value', self, 'float_value')
        else:
            self._check_button.set_active(False)
            adj = Gtk.Adjustment(0, 0, 0, 0, 0, 0)
            self._spin_button.set_adjustment(adj)
            self._spin_button.set_sensitive(False)
        self.add(self._spin_button)

    def _on_value_changed(self, spinbutton):
        changed = spinbutton.get_value_as_int() != self._original_priority
        self._check_button.set_active(changed)
        return False

    def conditionally_enable(self, policy_string):
        sensitive = policy_string in ('SCHED_FIFO', 'SCHED_RR')
        self.set_sensitive(sensitive)
        if sensitive and self._original_priority < 1:
            self.float_value = 1.0
        self._check_button.set_sensitive(sensitive)

    @GObject.property(type=float, default=1.0)
    def float_value(self):
        return float(self.selected_priority)

    @float_value.setter
    def float_value(self, value):
        try:
            self.selected_priority = int(value)
        except:
            pass

    @GObject.property(int, 0)
    def selected_priority(self):
        return self._priority

    @selected_priority.setter
    def selected_priority(self, value):
        self._priority = int(value)

    @property
    def unchanged(self):
        return not self._check_button.get_active()


class AffinityChooser(Gtk.Grid):
    unchanged_text = _('<Various>')

    def __init__(self, affinity, *args, **kwargs):
        super(AffinityChooser, self).__init__(visible=True,
                                              orientation='vertical',
                                              row_homogeneous=False,
                                              *args, **kwargs)
        self._affinity = affinity
        self._original_affinity = affinity
        self._check_button = Gtk.CheckButton(visible=True,
                                             label=_('A_ffinity'),
                                             hexpand=False, halign='start',
                                             use_underline=True)
        self._check_button.set_active(False)
        self.add(self._check_button)
        self._entry = Gtk.Entry(text=affinity, visible=True,
                                can_focus=True, expand=True,
                                halign='fill')
        self._entry.connect('changed', self._on_entry_changed)
        self._entry.connect('activate', self._on_entry_activate)
        self._entry.connect('focus-in-event', self._on_focus_in)
        self._entry.connect('button-release-event', self._on_focus_in)
        self._check_button.get_child().set_mnemonic_widget(self._entry)
        self.add(self._entry)
        self.set_column_homogeneous(False)

    def _on_entry_changed(self, _widget):
        text = self._entry.get_text()
        if text == self.unchanged_text:
            return False
        self.selected_affinity = text
        self._check_button.set_active(text != self._original_affinity)
        return False

    def _on_entry_activate(self, _widget):
        text = self._entry.get_text()
        try:
            affinity_bitmap = AffinityBitmap(text)
            text = affinity_bitmap.get_friendly_text()
            self._entry.set_text(text)
        except AffinityBitmap.ArgError:  # TODO: tell the user?
            pass
        self.selected_affinity = text
        self._check_button.set_active(text != self._original_affinity)
        return False

    def _on_focus_in(self, entry, _event):
        entry.select_region(0, -1)
        return False

    @GObject.property(str, '')
    def selected_affinity(self):
        return self._affinity

    @selected_affinity.setter
    def selected_affinity(self, value):
        self._affinity = value

    @property
    def unchanged(self):
        return not self._check_button.get_active()


class AttributesDialog(Gtk.Dialog):

    def __init__(self, parent, title):
        buttons = (_('_Cancel'), Gtk.ResponseType.CANCEL,
                   _('_Done'), Gtk.ResponseType.OK)
        super(AttributesDialog, self).__init__(visible=True,
                                               parent=parent,
                                               title=title,
                                               deletable=False,
                                               buttons=buttons)
        # making the button style match GtkMessageDialog (mostly)
        self.get_child().set_border_width(0)
        action_area = self.get_action_area()
        action_area.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        for button in action_area.get_children():
            button.get_child().set_property('margin', 10)


class LockButton(Gtk.LockButton):

    def __init__(self, **kwargs):
        super(LockButton, self).__init__(visible=True, **kwargs)
        self.set_focus_on_click(False)
        self._permission = Polkit.Permission.new_sync(INTERFACE_ACTION)
        self.set_permission(self._permission)

    @GObject.property(type=bool, default=False)
    def unlocked(self):
        return self._permission.get_allowed()


class _AdminResult(object):
    def __init__(self, successes=None, error=None):
        self._successes = successes
        self._error = error

    @property
    def succeeded(self):
        return self._error is None

    @property
    def successes(self):
        return self._successes

    @property
    def error_string(self):
        return self._error


class AdminProxy(object):
    _proxy = None
    _lock = threading.Lock()

    @classmethod
    def _get_proxy(cls):
        if cls._proxy is None:
            cls._proxy = Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SYSTEM,
                                                        Gio.DBusProxyFlags.NONE,
                                                        None,
                                                        BUS_NAME,
                                                        OBJECT_PATH,
                                                        INTERFACE_NAME)

    @classmethod
    def _proxy_error_handler(cls, _proxy, error, callback):
        GLib.idle_add(callback, _AdminResult(error=str(error)))
        cls._lock.release()

    @classmethod
    def _proxy_result_handler(cls, _proxy, result, callback):
        GLib.idle_add(callback, _AdminResult(successes=result))
        cls._lock.release()

    @classmethod
    def update_threads(cls, callback, thread_array):

        def run_proxy():
            cls._get_proxy()
            cls._proxy.UpdateThreads('(a(uiis))', thread_array,
                                     result_handler=cls._proxy_result_handler,
                                     error_handler=cls._proxy_error_handler,
                                     user_data=callback)
        cls._lock.acquire()
        threading.Thread(target=run_proxy).start()

    @classmethod
    def update_irqs(cls, callback, irq_array):

        def run_proxy():
            cls._get_proxy()
            cls._proxy.UpdateIRQs('(a(uuiis))', irq_array,
                                  result_handler=cls._proxy_result_handler,
                                  error_handler=cls._proxy_error_handler,
                                  user_data=callback)
        cls._lock.acquire()
        threading.Thread(target=run_proxy).start()



class PolledPIDStats(object):

    """A class for a single instance of procfs.pidstats() to be shared
    throughout the application. This class should not be instantiated,
    only its class methods should be called."""
    _pidstats = procfs.pidstats()
    _thread = None
    _timestamp = 0
    _lock = threading.Lock()

    @classmethod
    def pidstats(cls):
        cls._wait_for_it()
        return cls._pidstats

    @classmethod
    def process(cls, pid):
        return procfs.process(pid)

    @classmethod
    def reload(cls, lag=2):
        with cls._lock:
            prev = cls._timestamp
            now = int(time.time())
            if now - prev <= lag:
                return

            def _reload_pidstats():
                # This does I/O
                cls._pidstats.reload()
            if not cls._thread or not cls._thread.is_alive():
                cls._thread = threading.Thread(target=_reload_pidstats)
                cls._timestamp = now
                cls._thread.start()

    @classmethod
    def force_reload(cls):
        cls.reload(lag=-1000)
        cls._wait_for_it()

    @classmethod
    def reload_threads(cls):
        cls.pidstats().reload_threads()

    @classmethod
    def _wait_for_it(cls, timeout=60.0):
        if cls._thread.is_alive():
            cls._thread.join(timeout=timeout)
        if cls._thread.is_alive():
            raise TimeoutError

    @classmethod
    def rt_priority(cls, process):
        return int(process['stat']['rt_priority'])

    @classmethod
    def context_switches(cls, process):
        vsw = process['status']['voluntary_ctxt_switches']
        nvsw = process['status']['nonvoluntary_ctxt_switches']
        return vsw, nvsw

    @classmethod
    def find_by_regex(cls, irq_re):
        return cls.pidstats().find_by_regex(irq_re)

    @classmethod
    def has_context_switch(cls):
        return 'voluntary_ctxt_switches' in cls.pidstats()[1]['status']

    @classmethod
    def has_threaded_irqs(cls):
        irq_re = re.compile("(irq/[0-9]+-.+|IRQ-[0-9]+)")
        return len(cls.find_by_regex(irq_re)) > 0


# I have no real idea how perf works. This code copies the implementation
# from the Tuna GUI.
# TODO: I don't know how to stop and restart event monitoring if the user
# stops or starts refreshing.

class UnPolledPIDStats(PolledPIDStats):

    """A version of procfs.pidstats() backed up by perf event monitoring.
    reload() is a no-op if perf is available, otherwise this acts just
    like PolledPIDStats.
    There should be only one instance of this in the application"""

    def __init__(self):
        self._use_polling = True
        PolledPIDStats.force_reload()
        self._glib_source_tags = []
        try:
            import perf
            self._cpu_map = perf.cpu_map()
            thread_map = perf.thread_map()
            samples = perf.SAMPLE_CPU | perf.SAMPLE_TID
            evsel_cycles = perf.evsel(task=1, comm=1, wakeup_events=1,
                                      watermark=1, sample_type=samples)
            evsel_cycles.open(cpus=self._cpu_map, threads=thread_map)
            self._evlist = perf.evlist(self._cpu_map, thread_map)
            self._evlist.add(evsel_cycles)
            self._evlist.mmap()
            for fd in self._evlist.get_pollfd():
                tag = GLib.io_add_watch(fd, GLib.IOCondition.IN,
                                        self._process_events)
                self._glib_source_tags.append(tag)
            self._use_polling = False
        except:
            pass

    def __del__(self):
        # TODO: stop perf event monitoring (if it was started)
        for tag in tuple(self._glib_source_tags):
            try:
                GLib.source_remove(tag)
            except:
                pass
            del self._glib_source_tags[tag]

    def _process_events(self, *_args):
        import perf

        def record_fork(event):
            processes = self.pidstats().processes
            if event.pid == event.tid:
                try:
                    processes[event.pid] = procfs.process(event.pid)
                except:
                    pass
            else:
                try:
                    processes[event.pid].threads.processes[event.tid] = \
                        procfs.process(event.tid)
                except:
                    try:
                        processes[event.pid].threads = \
                            procfs.pidstats('/proc/%d/task/' % event.pid)
                    except:
                        pass
        re_read = True
        while re_read:
            re_read = False
            for cpu in self._cpu_map:
                event = self._evlist.read_on_cpu(cpu)
                if event:
                    re_read = True
                    if event.type == perf.RECORD_FORK:
                        record_fork(event)
                    elif event.type == perf.RECORD_EXIT:
                        del self.pidstats()[int(event.tid)]
        return True

    def reload(self, lag=2):
        if self._use_polling:
            PolledPIDStats.reload(lag)

    def rt_priority(self, process):
        if self._use_polling:
            return PolledPIDStats.rt_priority(process)
        stat = process['stat']
        stat.load()
        return int(stat['rt_priority'])

    def context_switches(self, process):
        if self._use_polling:
            return PolledPIDStats.context_switches(process)
        status = process['status']
        status.load()
        vswitch = status['voluntary_ctxt_switches']
        nvswitch = status['nonvoluntary_ctxt_switches']
        return vswitch, nvswitch


# This should not be instantiated. Just call the class methods.

class Interrupts(object):

    """A class for a single instance of procfs.interrupts().
    Only the one global instance created below should be used."""

    _interrupts = procfs.interrupts()
    _thread = None

    @classmethod
    def interrupts(cls):
        cls._wait_for_it()
        return cls._interrupts

    @classmethod
    def reload(cls, wait=False):
        def _reload_interrupts():
            cls._interrupts.reload()
        if not cls._thread or not cls._thread.is_alive():
            cls._thread = threading.Thread(target=_reload_interrupts)
            cls._thread.start()
        if wait:
            cls._wait_for_it()

    @classmethod
    def _wait_for_it(cls, timeout=10.0):
        cls._thread.join(timeout=timeout)
        if cls._thread.is_alive():
            raise TimeoutError

    @classmethod
    def events(cls, irq):
        return sum(cls.interrupts()[irq]['cpu'])

    @classmethod
    def irqs(cls):
        irqs = []
        for irq in cls.interrupts().keys():
            try:
                irqs.append(int(irq))
            except:
                pass
        return sorted(irqs)

    @classmethod
    def affinity(cls, irq):
        return AffinityBitmap(cls.interrupts()[irq]['affinity'])

    @classmethod
    def get_irq_users(cls, irq, nics):
        users = cls.interrupts()[irq]["users"]
        for u in users:
            if u in nics:
                try:
                    users[users.index(u)] = "%s(%s)" % (u, ethtool.get_module(u))
                except IOError:
                    # Old kernel, doesn't implement ETHTOOL_GDRVINFO
                    pass
        return users


Interrupts.reload()

# everyone can share one instance of the UnPolledPIDStats class
# (in theory, at least)
PIDStats = UnPolledPIDStats()
PIDStats.reload()

# One topology object for the whole application
Topology = hwloc.Topology()
Topology.ignore_type_keep_structure(hwloc.OBJ_CACHE)
flags = hwloc.TOPOLOGY_FLAG_WHOLE_SYSTEM | hwloc.TOPOLOGY_FLAG_IO_DEVICES
Topology.set_flags(flags)
Topology.load()

# One settings object for the whole application
Settings = Gio.Settings.new('org.fedora.pianofish')

# Global "quit" signal
AppQuitSignal = Signaler('AppQuitNow')

class AppQuitException(Exception):
    pass
