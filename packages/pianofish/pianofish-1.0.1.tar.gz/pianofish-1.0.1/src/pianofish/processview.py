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

from gi.repository import Gtk, Gdk, GObject, Pango

import fnmatch
import re
import errno

import hwloc
import schedutils
import procfs

from pianofish.utilities import WeightedTextRow, RowItem, PIDStats,\
    WeightedTextTreeView, WeightedTextTreeStore, TextRow, TextTreeView,\
    TextTreeStore, PolicyChooser, AffinityChooser, PriorityChooser,\
    AttributesDialog, AdminProxy, Settings, Topology, set_text_drag_icon
from pianofish.bitmap import AffinityBitmap


def _affinity_from_process(tid):
    return AffinityBitmap(schedutils.get_affinity(tid))

_InitialNumberAndColon = re.compile(r'^\d+:')


def _cgroup_list(pid):
    with open('/proc/' + str(pid) + '/cgroup') as cgroup_file:
        for line in cgroup_file:
            line = line.strip()
            if line.endswith('/'):
                continue
            line = _InitialNumberAndColon.sub('', line)
            yield line


def _no_ctxt_values(process, row, affinity):
    values = [None] * row.nr_columns
    pid = process['pid']
    values[row['PID']] = pid
    scheduler = schedutils.get_scheduler(pid)
    values[row['POLICY']] = schedutils.schedstr(scheduler)[6:]
    values[row['PRIORITY']] = PIDStats.rt_priority(process)
    if not affinity:
        affinity = _affinity_from_process(process)
    values[row['AFFINITY']] = affinity.get_friendly_text()
    values[row['CMDLINE']] = procfs.process_cmdline(process)
    return values


class _CtxSwitchViewRow(WeightedTextRow):
    def __init__(self):
        columns = (RowItem(_('PID'), 'PID', int),
                   RowItem(_('Policy'), 'POLICY', str),
                   RowItem(_('Priority'), 'PRIORITY', int),
                   RowItem(_('Affinity'), 'AFFINITY', str),
                   RowItem(_('Vol Ctxt\nSwitches'), 'VOLCTXT', int),
                   RowItem(_('NonVol\nSwitches'), 'NONVOLCTXT', int),
                   RowItem(_('Command Line'), 'CMDLINE', str,
                           (('expand', True), ('min-width', 200))))
        super(_CtxSwitchViewRow, self).__init__(columns)
        self.sort_column = self['PID']

    def new_values(self, process, affinity):
        values = _no_ctxt_values(process, self, affinity)
        vol, nonvol = PIDStats.context_switches(process)
        values[self['VOLCTXT']] = vol
        values[self['NONVOLCTXT']] = nonvol
        return values

    def cgroups_form(self, show_cgroups):
        return _CtxSwitchWithCgroups() if show_cgroups else self


class _CtxSwitchWithCgroups(WeightedTextRow):
    def __init__(self):
        columns = (RowItem(_('PID'), 'PID', int),
                   RowItem(_('Policy'), 'POLICY', str),
                   RowItem(_('Priority'), 'PRIORITY', int),
                   RowItem(_('Affinity'), 'AFFINITY', str),
                   RowItem(_('Vol Ctxt\nSwitches'), 'VOLCTXT', int),
                   RowItem(_('NonVol\nSwitches'), 'NONVOLCTXT', int),
                   RowItem(_('Cgroups'), 'CGROUPS', str,
                           cell_props=(('ellipsize',
                                        Pango.EllipsizeMode.END),
                                       ('max-width-chars', 48))),
                   RowItem(_('Command Line'), 'CMDLINE', str,
                           (('expand', True), ('min-width', 200))))
        super(_CtxSwitchWithCgroups, self).__init__(columns)
        self.sort_column = self['PID']

    def new_values(self, process, affinity):
        values = _no_ctxt_values(process, self, affinity)
        vol, nonvol = PIDStats.context_switches(process)
        values[self['VOLCTXT']] = vol
        values[self['NONVOLCTXT']] = nonvol
        cgroups = _(',').join(_cgroup_list(process.pid))
        if not cgroups:
            cgroups = _('<default>')
        values[self['CGROUPS']] = cgroups
        return values

    def cgroups_form(self, show_cgroups):
        return self if show_cgroups else _CtxSwitchViewRow()


class _NoCtxSwitchViewRow(WeightedTextRow):
    def __init__(self):
        columns = (RowItem(_('PID'), 'PID', int),
                   RowItem(_('Policy'), 'POLICY', str),
                   RowItem(_('Priority'), 'PRIORITY', int),
                   RowItem(_('Affinity'), 'AFFINITY', str),
                   RowItem(_('Command Line'), 'CMDLINE', str,
                           (('max-width', 200), ('expand', True))))
        super(_NoCtxSwitchViewRow, self).__init__(columns)
        self.sort_column = self['PID']

    def new_values(self, process, affinity):
        return _no_ctxt_values(process, self, affinity)

    def cgroups_form(self, show_cgroups):
        return _NoCtxSwitchWithCgroups() if show_cgroups else self


class _NoCtxSwitchWithCgroups(WeightedTextRow):
    def __init__(self):
        columns = (RowItem(_('PID'), 'PID', int),
                   RowItem(_('Policy'), 'POLICY', str),
                   RowItem(_('Priority'), 'PRIORITY', int),
                   RowItem(_('Affinity'), 'AFFINITY', str),
                   RowItem(_('Cgroups'), 'CGROUPS', str),
                   RowItem(_('Command Line'), 'CMDLINE', str,
                           (('max-width', 200), ('expand', True))))
        super(_NoCtxSwitchWithCgroups, self).__init__(columns)
        self.sort_column = self['PID']

    def new_values(self, process, affinity):
        values = _no_ctxt_values(process, self, affinity)
        values[self['CGROUPS']] = _(',').join(_cgroup_list(process.pid))

    def cgroups_form(self, show_cgroups):
        return self if show_cgroups else _NoCtxSwitchViewRow()


class _AttributesDialogRow(TextRow):
    def __init__(self):
        columns = (RowItem(_('PID'), 'PID', int),
                   RowItem(_('Command Line'), 'CMDLINE', str,
                           (('expand', True),)))
        super(_AttributesDialogRow, self).__init__(columns)

        self.sort_column = self['PID']


class _ProcessAttributesDialog(AttributesDialog):

    def __init__(self, parent, view):
        title = _('Set Process Attributes')
        super(_ProcessAttributesDialog, self).__init__(parent=parent,
                                                       title=title)
        process_list = view
        main_grid = Gtk.Grid(visible=True, expand=True, border_width=5,
                             row_homogeneous=False,
                             orientation='vertical')
        label = Gtk.Label(_('Adjust the listed processes:'), visible=True,
                          halign='start', margin_start=5, margin_top=15)
        main_grid.add(label)
        if process_list.not_all_threads:
            label = Gtk.Label(_('<b>Not all threads have been selected for some processes</b>'),
                              use_markup=True, visible=True, halign='fill', valign='start')
            main_grid.add(label)
        scrolled_window = Gtk.ScrolledWindow(hscrollbar_policy='automatic',
                                             vscrollbar_policy='automatic',
                                             expand=True, visible=True,
                                             shadow_type='in',)
        scrolled_window.add(process_list)
        main_grid.add(scrolled_window)
        label = Gtk.Label(_('<i>Only attributes with a checked box will be changed</i>'),
                          visible=True, halign='fill', valign='start',
                          margin_bottom=10, margin_top=20, use_markup=True)
        main_grid.add(label)
        attributes_grid = Gtk.Grid(visible=True, hexpand=True,
                                   vexpand=False,
                                   valign='end', halign='fill',
                                   column_homogeneous=False,
                                   column_spacing=30,
                                   margin_bottom=10,
                                   orientation='horizontal')

        def all_the_same(entry, default):
            array = list(set([v[entry] for v in process_list.full_values_array]))
            if len(array) == 1:
                return array[0]
            return default
        self._priority = all_the_same(process_list.full_values_columns['PRIORITY'],
                                      PriorityChooser.unchanged_text)
        self._priority_chooser = PriorityChooser(self._priority,
                                                 expand=False,
                                                 valign='center',
                                                 halign='start')
        self._priority_chooser.bind_property('selected_priority', self,
                                             'priority',
                                             GObject.BindingFlags.SYNC_CREATE)
        self._policy = all_the_same(process_list.full_values_columns['POLICY'],
                                    PolicyChooser.unchanged_text)
        self._policy_chooser = PolicyChooser(self._policy,
                                             valign='center',
                                             halign='start')
        self._policy_chooser.bind_property('selected_policy', self,
                                           'policy')
        attributes_grid.add(self._policy_chooser)
        self._priority_chooser.conditionally_enable('SCHED_' + self._policy)
        attributes_grid.add(self._priority_chooser)
        self._affinity = all_the_same(process_list.full_values_columns['AFFINITY'],
                                      AffinityChooser.unchanged_text)
        self._affinity_chooser = AffinityChooser(self._affinity,
                                                 expand=True,
                                                 valign='center',
                                                 halign='fill')
        self._affinity_chooser.bind_property('selected_affinity', self,
                                             'affinity')
        attributes_grid.add(self._affinity_chooser)
        main_grid.add(attributes_grid)
        self.get_content_area().add(main_grid)

    @GObject.property(str, '')
    def policy(self):
        return self._policy

    @policy.setter
    def policy(self, value):
        self._policy = value
        self._priority_chooser.conditionally_enable(value)

    @property
    def policy_changed(self):
        return not self._policy_chooser.unchanged

    @GObject.property(int, 1)
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        try:
            self._priority = int(value)
        except ValueError:
            pass

    @property
    def priority_changed(self):
        return not self._priority_chooser.unchanged

    @GObject.property(str, '')
    def affinity(self):
        return self._affinity

    @affinity.setter
    def affinity(self, value):
        self._affinity = value

    @property
    def affinity_changed(self):
        return not self._affinity_chooser.unchanged


class _DistributeDialog(AttributesDialog):

    def __init__(self, parent, selection_view, cpu_selection_string, npids):
        title = _('Set Process Attributes')
        self.title = _('Distribute Tasks')
        super(_DistributeDialog, self).__init__(parent=parent,
                                                title=title)

        self._npids = npids
        self._distribution = None
        self._selection_bitmap = AffinityBitmap(cpu_selection_string)
        self._topology = Topology
        self._start_box = Gtk.ComboBoxText(visible=True)
        self._end_box = Gtk.ComboBoxText(visible=True)
        self._start_handler_id = self._start_box.connect('changed', self._on_start_changed)
        self._end_handler_id = self._end_box.connect('changed', self._on_end_changed)
        self._update_boxes()

        main_grid = Gtk.Grid(visible=True, expand=True, border_width=15,
                             row_homogeneous=False,
                             column_homogeneous=True,
                             orientation='vertical')
        label = Gtk.Label(_('<b>Distribute the listed threads across CPUs</b>'),
                          visible=True, halign='start', use_markup=True,
                          margin_top=5, margin_bottom=0)
        main_grid.add(label)
        label = _('_Restrict distribution to selected processor set: ') + cpu_selection_string
        self._restrict_checkbutton = Gtk.CheckButton(label, visible=False,
                                                     use_underline=True,
                                                     margin_start=15)
        self._restrict_checkbutton.connect('clicked', self._restriction_changed)
        main_grid.add(self._restrict_checkbutton)
        if Topology.cpuset != self._selection_bitmap:
            self._restrict_checkbutton.show()
        label = _('_Assign each thread to only one processor')
        self._singlify_button = Gtk.CheckButton(label, visible=True,
                                                use_underline=True,
                                                margin_start=15)
        main_grid.add(self._singlify_button)
        range_grid = Gtk.Grid(visible=True, expand=True, halign='start',
                              margin_bottom=10, margin_top=15, column_spacing=30,
                              row_homogeneous=False,
                              column_homogeneous=True)
        label = Gtk.Label(_('_Start distribution at:'), visible=True, use_underline=True)
        label.set_mnemonic_widget(self._start_box)
        range_grid.add(label)
        label = Gtk.Label(_('_End distribution at:'), visible=True, use_underline=True)
        label.set_mnemonic_widget(self._end_box)
        range_grid.attach(label, 1, 0, 1, 1)
        range_grid.attach(self._start_box, 0, 1, 1, 1)
        range_grid.attach(self._end_box, 1, 1, 1, 1)
        main_grid.add(range_grid)
        if selection_view.not_all_threads:
            label = Gtk.Label(_('<b>Not all threads have been selected for some processes</b>'),
                              use_markup=True, visible=True, halign='fill', valign='start')
            main_grid.add(label)

        scrolled_window = Gtk.ScrolledWindow(hscrollbar_policy='automatic',
                                             vscrollbar_policy='automatic',
                                             expand=True, visible=True,
                                             shadow_type='in')
        scrolled_window.add(selection_view)
        main_grid.add(scrolled_window)
        self.get_content_area().add(main_grid)

    def do_response(self, rid):
        if rid == Gtk.ResponseType.OK:
            drange = tuple(self._topology.objs_by_depth(self._start_depth))
            self._distribution = self._topology.distrib(drange, self._npids,
                                                        hwloc.INT_MAX, 0)
            if self._singlify_button.get_active():
                for bitmap in self._distribution:
                    bitmap.singlify()

    def _update_boxes(self):
        useful_depths = []
        for d in range(self._topology.depth):
            if Topology.get_nbobjs_by_depth(d) != 0:
                obj = self._topology.get_next_obj_by_depth(d, None)
                if not obj.cpuset.iszero:
                    useful_depths.append(d)
        self._depths = tuple(useful_depths)
        self._start_depth = self._depths[0]
        self._end_depth = self._depths[-1]
        self._populate_box(self._start_box, self._start_handler_id, self._depths, self._start_depth)
        self._populate_box(self._end_box, self._end_handler_id, self._depths, self._end_depth)

    def _restriction_changed(self, button):
        if button.get_active():
            bm = AffinityBitmap(self._selection_bitmap)
            self._topology = Topology.dup()
            self._topology.restrict(bm, hwloc.RESTRICT_FLAG_ADAPT_IO)
        else:
            self._topology = Topology
        self._update_boxes()

    def _populate_box(self, box, hid, depths, index):
        with box.handler_block(hid):
            box.remove_all()
            for depth in depths:
                text = hwloc.Obj.string_of_type(self._topology.get_depth_type(depth))
                box.append_text(text)
                box.set_active(index)

    def _on_start_changed(self, box):
        text = box.get_active_text()
        start_depth = self._topology.get_type_depth(hwloc.Obj.type_sscanf(text)[0])
        self._start_depth = start_depth
        end_depth = self._end_depth
        if end_depth < start_depth:
            end_depth = start_depth
        new_depths = self._depths[start_depth:]
        new_index = new_depths.index(end_depth)
        self._populate_box(self._end_box, self._end_handler_id, new_depths, new_index)

    def _on_end_changed(self, box):
        text = box.get_active_text()
        end_depth = self._topology.get_type_depth(hwloc.Obj.type_sscanf(text)[0])
        self._end_depth = end_depth
        start_depth = self._start_depth
        if end_depth < start_depth:
            start_depth = end_depth
        new_depths = self._depths[:end_depth+1]
        new_index = new_depths.index(start_depth)
        self._populate_box(self._start_box, self._start_handler_id, new_depths, new_index)

    @property
    def distribution(self):
        return self._distribution


class _FilterBox(Gtk.Grid):

    def __init__(self, changed_handler, **kwargs):
        super(_FilterBox, self).__init__(visible=True,
                                         column_homogeneous=False,
                                         orientation='horizontal',
                                         **kwargs)
        label = Gtk.Label(_('Commandline _filter:'),
                          visible=True, use_underline=True,
                          halign='start', margin_end=3)
        self.add(label)
        entry = Gtk.SearchEntry(visible=True, text='', can_focus=True,
                                expand=True, halign='fill', margin=2)
        entry.connect('search-changed', changed_handler)
        label.set_mnemonic_widget(entry)
        self.add(entry)
        self._entry = entry
        self.get_text = entry.get_text
        self.focus_entry = entry.grab_focus

    @GObject.property(type=str, default='')
    def placeholder_text(self):
        return self._entry.get_placeholder_text()

    @placeholder_text.setter
    def placeholder_text(self, value):
        self._entry.set_placeholder_text(value)


class _SelectionTreeView(TextTreeView):

    def __init__(self, process_view, process_row, selection, x, y):
        self._selection_row = _AttributesDialogRow()
        super(_SelectionTreeView, self).__init__(self._selection_row, visible=True)
        self._full_row = process_row
        process_store = process_view.get_model()
        rows = selection.get_selected_rows()[1]
        if not rows:
            rows = [process_view.get_path_at_pos(x, y)[0]]
        pidstats = PIDStats.pidstats()
        tgids = {}
        self.get_selection().set_mode(Gtk.SelectionMode.NONE)
        model = TextTreeStore(self._selection_row)
        self.set_model(model=model)
        thread_coverage = []
        thread = None
        self.full_values_array = []
        column_keys = tuple(c.keyword for c in self._selection_row.columns)
        column_range = range(process_row.nr_columns)
        # This pass adds thread group leaders to the selection view.
        # It also adds a TGID's other threads, if the selected row is not expanded.
        for path in rows:
            tree_iter = process_store.get_iter(path)
            pid = process_store.get_value(tree_iter, self._selection_row['PID'])
            try:
                thread = pidstats[pid]
            except KeyError:
                # only thread group leaders here
                continue
            values = process_store.get(tree_iter, *column_range)
            self.full_values_array.append(values)
            values = tuple(values[process_row[key]] for key in column_keys)
            row_iter = model.append(None)
            model.set_row_values(row_iter, values)
            tgids[pid] = row_iter
            if not process_view.row_expanded(path):
                child_iter = process_store.iter_children(tree_iter)
                while child_iter:
                    values = process_store.get(child_iter, *column_range)
                    self.full_values_array.append(values)
                    values = tuple(values[process_row[key]] for key in column_keys)
                    model_child_iter = model.append(row_iter)
                    model.set_row_values(model_child_iter, values)
                    child_iter = process_store.iter_next(child_iter)
            else:
                # Keep track of threads in expanded rows, so we can tell
                # if they are all selected
                thread.load_threads()
                thread_coverage += thread.threads.keys()

        fake_tgids = {}
        # This pass adds non-TGID selections. These will only be selected threads
        # from expanded rows.
        for path in rows:
            expandit = False
            tree_iter = process_store.get_iter(path)
            pid = process_store.get_value(tree_iter, process_row['PID'])
            if pid in tgids:
                # Already added above.
                continue
            try:
                tgid = PIDStats.process(pid)['status']['Tgid']
            except KeyError:
                # Thread might have gone away.
                thread_coverage.remove(pid)
                continue
            if tgid in tgids:
                # Thread whose TGID has already been added
                parent = tgids[tgid]
            elif tgid in fake_tgids:
                # Thread with unselected TGID, but another thread of this
                # process has been added
                parent = fake_tgids[tgid]
            else:
                # Thread with unselected TGID, and no other thread of this process
                # has yet been added.
                parent = model.append(None)
                # We will expand this row in the selection view
                expandit = True
                # Make a fake TGID entry as the top level for this row
                model.set_value(parent, self._selection_row['PID'], -1)
                model.set_value(parent, self._selection_row['CMDLINE'], _('* the thread group leader is not selected *'))
                fake_tgids[tgid] = parent
                # Keep track of the threads in this process, so we can warn
                # if some are unselected.
                pp = PIDStats.process(tgid)
                pp.load_threads()
                thread_coverage += pp.threads.keys()
            values = process_store.get(tree_iter, *column_range)
            self.full_values_array.append(values)
            row_iter = model.append(parent)
            values = tuple(values[process_row[key]] for key in column_keys)
            model.set_row_values(row_iter, values)
            if expandit:
                self.expand_row(model.get_path(parent), True)
            tgids[pid] = row_iter
            # Remove this thread from the coverage list
            thread_coverage.remove(pid)
        # not_all_threads means at least one selected process has a thread
        # that is not selected.
        self.not_all_threads = len(thread_coverage) != 0

    @property
    def value_columns(self):
        return self._selection_row

    @property
    def full_values_columns(self):
        return self._full_row

class ProcessView(Gtk.Grid):

    def __init__(self, **kwargs):
        super(ProcessView, self).__init__(visible=True,
                                          orientation='vertical',
                                          **kwargs)
        self._filter_mode = False
        self._refreshing = True
        self._cpu_selection = None
        self._show_cgroups = Settings.get_boolean('cgroups')
        self._treeview = _ProcessTreeView(margin=0)
        self.bind_property('refreshing', self._treeview, 'refreshing',
                           GObject.BindingFlags.DEFAULT)
        scroll = Gtk.ScrolledWindow(visible=True, margin=0,
                                    vscrollbar_policy='automatic',
                                    hscrollbar_policy='automatic',
                                    shadow_type='in',
                                    expand=True)
        scroll.add(self._treeview)
        self.add(scroll)
        self._scrolled_window = scroll
        # I could not get a Gtk SearchBar to work here.
        self._filter_box = _FilterBox(self._search_changed)
        revealer = Gtk.Revealer(visible=True,
                                transition_type='slide-up',
                                hexpand=True, vexpand=False)
        revealer.add(self._filter_box)
        self.bind_property('filter-mode', revealer, 'reveal-child')
        revealer.connect('notify::child-revealed',
                         self._on_notify_revealer_revealed)
        self.add(revealer)

    @GObject.property(type=bool, default=False)
    def filter_mode(self):
        return self._filter_mode

    @filter_mode.setter
    def filter_mode(self, value):
        refresh = value != self._filter_mode
        self._filter_mode = value
        if refresh:
            self.refresh(self._cpu_selection)

    @GObject.property(type=bool, default=True)
    def refreshing(self):
        return self._refreshing

    @refreshing.setter
    def refreshing(self, value):
        self._refreshing = bool(value)

    def refresh(self, cpu_selection):
        self._cpu_selection = cpu_selection
        if self._filter_mode:
            filter_text = self._filter_box.get_text()
            if Settings.get_boolean('glob'):
                if filter_text:
                    if r'*?\[]' not in filter_text:
                        filter_text += '*'
                    filter_text = fnmatch.translate(filter_text)
        else:
            filter_text = ''
        return self._treeview.refresh(cpu_selection, filter_text)

    def _on_notify_revealer_revealed(self, _widget, _param):
        if self.filter_mode:
            self._filter_box.focus_entry()

    def _search_changed(self, _widget):
        self.refresh(self._cpu_selection)

    def settings_changed(self):
        if Settings.get_boolean('glob'):
            self._filter_box.placeholder_text = _('Bash-style glob')
        else:
            self._filter_box.placeholder_text = _('Regular Expression')
        show_cgroups = Settings.get_boolean('cgroups')
        if self._show_cgroups != show_cgroups:
            self._show_cgroups = show_cgroups
            self._scrolled_window.remove(self._treeview)
            self._treeview = _ProcessTreeView(margin=0)
            self._scrolled_window.add(self._treeview)
        else:
            self._treeview.settings_changed()

    def handle_dropped_text(self, text, cpu_selection):
        return self._treeview.handle_dropped_text(text, cpu_selection)


class _ProcessTreeView(WeightedTextTreeView):

    def __init__(self, **kwargs):
        row = _CtxSwitchViewRow() \
            if PIDStats.has_context_switch() else _NoCtxSwitchViewRow()
        self._row = row.cgroups_form(Settings.get_boolean('cgroups'))
        super(_ProcessTreeView, self).__init__(self._row, visible=True,
                                               **kwargs)
        self.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self._cpu_selection = None
        self._filter_text = ''
        self._visible_pid = None
        self._visible_row = None
        self._refreshing = True
        self._button_press_x = None
        self._button_press_y = None
        self._referenced_cell = None
        self._show_uthreads = Settings.get_boolean('uthreads')
        self._show_kthreads = Settings.get_boolean('kthreads')
        self.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [],
                                      Gdk.DragAction.COPY)
        self.drag_source_add_text_targets()
        self.connect('drag-data-get', self._on_drag_data_get)
        self._tree_store = WeightedTextTreeStore(self._row)
        self.set_model(self._tree_store)
        label = _('_Refresh the process list')
        self._refresh_checkbox = Gtk.CheckMenuItem(label=label,
                                                   visible=True,
                                                   use_underline=True)
        self.bind_property('refreshing', self._refresh_checkbox, 'active',
                           GObject.BindingFlags.BIDIRECTIONAL |
                           GObject.BindingFlags.SYNC_CREATE)
        self._popup_menu = Gtk.Menu(visible=True)
        menu_item = Gtk.MenuItem(label=_('_Set process attributes'),
                                 visible=True, use_underline=True)
        menu_item.connect('activate', self._on_edit_activated)
        self._popup_menu.add(menu_item)
        menu_item = Gtk.MenuItem(label=_('_Distribute tasks'),
                                 visible=True, use_underline=True)
        menu_item.connect('activate', self._on_distribute_activated)
        self._popup_menu.add(menu_item)
        self._popup_menu.add(self._refresh_checkbox)

    def settings_changed(self):
        self._show_uthreads = Settings.get_boolean('uthreads')
        self._show_kthreads = Settings.get_boolean('kthreads')
        if self._cpu_selection:
            self._refresh(self._cpu_selection, self._filter_text)
        return

    @GObject.property(type=bool, default=True)
    def refreshing(self):
        return self._refreshing

    @refreshing.setter
    def refreshing(self, value):
        self._refreshing = bool(value)

    def do_button_press_event(self, event):
        self._button_press_x = event.x
        self._button_press_y = event.y
        if event.type == Gdk.EventType.BUTTON_PRESS \
                and event.button == Gdk.BUTTON_SECONDARY:
            self._popup_menu.popup(None, None, None, None, event.button,
                                   event.time)
            return True
        # using super() here causes infinite recursion?
        return WeightedTextTreeView.do_button_press_event(self, event)

    def _update_callback(self, result):
        if result.succeeded:
            pids = ', '.join(str(pid) for pid in result.successes)
            message = _('Attribute changes succeeded for PIDs: {pids}')
            message = message.format(pids=pids)
        else:
            message = result.error_string
        label = Gtk.Label(label=message, visible=True, wrap=True,
                          margin_top=12, margin_bottom=12,
                          margin_start=5, margin_end=5)
        popover = Gtk.Popover.new(self)
        rect = Gdk.Rectangle()
        rect.x = self._button_press_x
        rect.y = self._button_press_y
        rect.x, rect.y = self.convert_bin_window_to_widget_coords(rect.x,
                                                                  rect.y)
        popover.set_pointing_to(rect)
        popover.add(label)
        popover.show()
        if self._cpu_selection is not None:
            self.refresh(self._cpu_selection, self._filter_text)

    def _on_edit_activated(self, _widget):
        path = self.get_path_at_pos(self._button_press_x,
                                    self._button_press_y)[0]
        if not path:
            return
        selection = self.get_selection()
        treeview = _SelectionTreeView(self, self._row, selection,
                                      self._button_press_x,
                                      self._button_press_y)

        dialog = _ProcessAttributesDialog(self.get_toplevel(), treeview)
        result = dialog.run()
        dialog.destroy()
        if result != Gtk.ResponseType.OK:
            return
        new_affinity = ''
        try:
            if dialog.affinity_changed:
                new_affinity = AffinityBitmap(dialog.affinity)
        except AffinityBitmap.ArgError:
            text = _('Unable to parse affinity specification')
            errdialog = Gtk.MessageDialog(parent=self.get_toplevel(),
                                          title='pianofish',
                                          text=text,
                                          secondary_text=dialog.affinity,
                                          buttons=Gtk.ButtonsType.CLOSE)
            errdialog.run()
            errdialog.destroy()
            return
        if dialog.policy_changed:
            new_policy = schedutils.schedfromstr(dialog.policy)
            new_priority = dialog.priority
        else:
            new_policy = -1
            new_priority = dialog.priority if dialog.priority_changed else -1
        thread_array = [(values[self._row['PID']],
                         new_policy,
                         new_priority,
                         str(new_affinity))
                        for values in treeview.full_values_array]
        AdminProxy.update_threads(self._update_callback, thread_array)

    def _on_distribute_activated(self, _widget):
        path = self.get_path_at_pos(self._button_press_x,
                                    self._button_press_y)[0]
        if not path:
            return
        selection = self.get_selection()
        selection_view = _SelectionTreeView(self, self._row, selection,
                                            self._button_press_x,
                                            self._button_press_y)

        pids = tuple(values[self._row['PID']] for values in selection_view.full_values_array)
        dialog = _DistributeDialog(self.get_toplevel(), selection_view,
                                   self._cpu_selection, len(pids))
        result = dialog.run()
        sets = dialog.distribution
        dialog.destroy()
        if result != Gtk.ResponseType.OK:
            return
        thread_array = [(pids[i], -1, -1, str(sets[i])) for i in range(len(pids))]
        AdminProxy.update_threads(self._update_callback, thread_array)

    def _update_rows(self, selected_bitmap, pidstat_array, row_iter,
                     parent_iter):

        def is_kernel_thread(process_):
            filename = '/proc/%d/smaps' % (process_.pid,)
            try:
                with open(filename) as smapsfile:
                    line = smapsfile.readline()
            except IOError as error:
                if error.errno == errno.EACCES:
                    # This doesn't work without privileges.
                    return False
                raise error
            if line:
                return False
            pidstat = procfs.pidstat(process_.pid)
            if pidstat['state'] == 'Z':
                return False
            return True

        def show_this_thread(tid_affinity_, selected_bitmap_, thread_):
            if not tid_affinity_.iszero \
                    and not tid_affinity.intersects(selected_bitmap_):
                return False
            if self._show_kthreads and self._show_uthreads:
                return True
            kthread = is_kernel_thread(thread_)
            if self._show_kthreads and kthread:
                return True
            return self._show_uthreads and not kthread

        # make a local copy, unique and sorted.
        thread_list = list(sorted(set(pidstat_array.keys())))
        while row_iter:
            row_values = self._tree_store.get(row_iter,
                                              *range(self._row.nr_columns))
            row_tid = row_values[self._row['PID']]
            # See if this pid is no longer around (or filtered out)
            try:
                thread_list.remove(row_tid)
                thread = pidstat_array[row_tid]
                tid_affinity = _affinity_from_process(row_tid)
            except:
                if self._tree_store.remove(row_iter):
                    # there is another row
                    continue
                # there are no more rows
                break

            # If this row's affinity does not include CPUs in our CPU
            # filter, remove the row from the thread list and the list_store.
            if not show_this_thread(tid_affinity, selected_bitmap,
                                    thread):
                try:
                    thread_list.remove(row_tid)
                except ValueError:
                    # this row was not in the thread list
                    pass
                if self._tree_store.remove(row_iter):
                    # there is another row
                    continue
                # there are no more rows
                break
            # If we get to here, the row is represents a current thread
            # that is not filtered out
            current_values = self._row.new_values(thread, tid_affinity)
            try:
                self._tree_store.set_row_values(row_iter, current_values)
            except:
                if self._tree_store.remove(row_iter):
                    continue
                break
            if row_tid == self._visible_pid:
                self._visible_row = row_iter
            if not parent_iter:
                try:
                    thread.load_threads()
                    children = thread['threads']
                except KeyError:
                    children = {}
                child_iter = self._tree_store.iter_children(row_iter)
                try:
                    self._update_rows(selected_bitmap, children,
                                      child_iter, row_iter)
                except:
                    pass
            row_iter = self._tree_store.iter_next(row_iter)
        # All that remains now in thread_list is threads new since the last
        # update. Add them at the end
        for tid in thread_list:
            try:
                thread = pidstat_array[tid]
                # make sure the TGID is at the top of a thread list
                if parent_iter is None and tid != thread['status']['Tgid']:
                    continue
                tid_affinity = _affinity_from_process(tid)
            except:
                # thread went away
                continue
            if not show_this_thread(tid_affinity, selected_bitmap,
                                    thread):
                continue
            try:
                current_values = self._row.new_values(thread, tid_affinity)
            except:
                continue
            thread_iter = self._tree_store.append(parent_iter)
            try:
                self._tree_store.set_row_values(thread_iter, current_values)
            except:
                self._tree_store.remove(thread_iter)
                continue
            if parent_iter is not None:
                continue
            try:
                thread.load_threads()
                children = thread['threads']
            except KeyError:
                continue
            self._update_rows(selected_bitmap, children, None,
                              thread_iter)

    def refresh(self, cpu_selection, filter_text):
        if self.refreshing:
            return self._refresh(cpu_selection, filter_text)

    def _refresh(self, cpu_selection, filter_text):
        self._cpu_selection = cpu_selection
        new_filter = filter_text != self._filter_text
        self._filter_text = filter_text
        PIDStats.reload()
        PIDStats.reload_threads()
        selected_bitmap = AffinityBitmap(cpu_selection)
        row_iter = self._tree_store.get_iter_first()
        if row_iter and new_filter:
            self._visible_pid = self._tree_store.get_value(row_iter,
                                                           self._row['PID'])
        else:
            self._visible_pid = None
        self._visible_row = None
        pidstats = PIDStats.pidstats()
        if filter_text:
            try:
                regex = re.compile(filter_text)
                pids = {}
                for pid in pidstats.find_by_cmdline_regex(regex):
                    pids[pid] = pidstats[pid]
                pidstats = pids
            except:
                pidstats = {}
        self._update_rows(selected_bitmap, pidstats, row_iter,
                          None)
        if self._visible_row:
            path = self._tree_store.get_path(self._visible_row)
            self.scroll_to_cell(path, None, False, 0.0, 0.0)

    def _on_drag_data_get(self, _widget, _context, selection_data,
                          _info, _time):
        selection_data.set_text('process:set selection to bitmap', -1)
        return True

    def do_drag_begin(self, context):
        selection = self.get_selection()

        pids = []
        def foreach_selected_cb(model, path, iter_):
            pids.append(str(model.get_value(iter_, self._row['PID'])))
            if not self.row_expanded(path):
                child_iter = self._tree_store.iter_children(iter_)
                while child_iter:
                    pids.append(str(model.get_value(child_iter,
                                                    self._row['PID'])))
                    child_iter = self._tree_store.iter_next(child_iter)

        selection.selected_foreach(foreach_selected_cb)
        string = 'PID: ' + ','.join(pids)
        set_text_drag_icon(self, context, string)
        return True

    def handle_dropped_text(self, text, cpu_selection):
        if text != 'set selection to bitmap':
            return
        selection = self.get_selection()
        affinity_string = str(AffinityBitmap(cpu_selection))

        thread_array = []
        def foreach_selected_cb(model, path, iter_):
            pid = model.get_value(iter_, self._row['PID'])
            thread_array.append((pid, -1, -1, affinity_string))
            if not self.row_expanded(path):
                child_iter = self._tree_store.iter_children(iter_)
                while child_iter:
                    pid = model.get_value(child_iter, self._row['PID'])
                    thread_array.append((pid, -1, -1, affinity_string))
                    child_iter = self._tree_store.iter_next(child_iter)

        selection.selected_foreach(foreach_selected_cb)
        AdminProxy.update_threads(self._update_callback, thread_array)
