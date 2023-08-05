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

from gi.repository import Gtk, GObject, GLib
import hwloc
import procfs
import threading

from pianofish.pciview import PCIView
from pianofish.utilities import Signaler, Topology, AppQuitException
from pianofish.bitmap import AffinityBitmap


def _header_string(obj, verbose=0):
    objstring = obj.type_asprintf(verbose)
    if objstring.startswith('Group'):  # text comes from hwloc - not translated
        subgroup = obj.first_child.type_asprintf(0)
        return _('Group of {subgroup:s}').format(subgroup=subgroup)
    if obj.depth != 0:
        if obj.os_index != hwloc.UINT_MAX:
            objstring += ' ' + str(obj.os_index)
    attr = obj.attr_asprintf(' ', verbose)
    if attr:
        objstring += ' (' + attr + ')'
    if obj.arity != 0:
        thisgroup = '<i>' + objstring + '</i>'
        # type names are untranslated, so adding 's' for plural works
        childtypes = '<b>' + obj.first_child.type_asprintf(0) + 's</b>'
        return _('{childtypes:s} in {thisgroup:s}').format(thisgroup=thisgroup,
                                                           childtypes=childtypes)
    return objstring


def _obj_index_string(obj):
    objstring = obj.type_asprintf(0)
    if objstring.startswith('Group'):
        objstring = objstring[len('Group'):]
    if obj.depth != 0:
        if obj.os_index != hwloc.UINT_MAX:
            objstring = str(obj.os_index)
    return objstring


def _string_of_numbers(nums):
    bmap = AffinityBitmap(set(nums))
    return bmap.get_friendly_text(list_max=24)


class UsageLevelBar(Gtk.LevelBar):

    def __init__(self, *args, **kwargs):
        super(UsageLevelBar, self).__init__(max_value=100.0,
                                            min_value=0.0,
                                            value=0.0,
                                            can_focus=False,
                                            margin=8,
                                            *args, **kwargs)
        self._usage = 0.0

    @GObject.property(type=float, default=0.0, minimum=0.0, maximum=100.0)
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, value):
        self._usage = value
        self.set_value(value)


class _ObjectView(Gtk.Grid):

    def __init__(self, obj, listbox, parent):
        super(_ObjectView, self).__init__(visible=True, vexpand=False,
                                          hexpand=True, column_homogeneous=False,
                                          row_homogeneous=False,
                                          column_spacing=3,
                                          orientation='horizontal',
                                          border_width=3, valign='start')
        self.__hwloc_obj = obj
        self.parent = parent
        self._usage = 0.0
        listbox.add(self)
        index_width = parent.child_index_width if parent else 1
        label = _obj_index_string(obj)
        self.add(Gtk.Label(label=label, use_markup=True,
                           width_chars=index_width, xalign=1.0,
                           visible=True, expand=False, halign='fill'))
        child_objs = [o for o in obj.children if
                      o.depth >= 0 and o.type in _VIEWS_BY_TYPE]
        self.child_index_width = 0
        if child_objs:
            indexes = [o.os_index for o in child_objs
                       if o.os_index != hwloc.UINT_MAX]
            indexes.append(1)
            self.child_index_width = len(str(max(indexes)))
        self.offspring = tuple([_type_view(c, listbox, self)
                                for c in child_objs])
        self._level_bar = UsageLevelBar(visible=True, vexpand=False,
                                        hexpand=True, halign='fill')
        self.bind_property('usage', self._level_bar, 'usage')
        self.add(self._level_bar)
        self._check_button = Gtk.CheckButton(visible=True, sensitive=False,
                                             halign='end')
        self._check_button.connect('toggled', self._check_button_toggled)
        self.add(self._check_button)
        if self.offspring:
            nums = [o.hwloc_object.os_index for o in self.offspring]
            if -1 in nums:
                nums = str(nums)
            else:
                nums = _string_of_numbers(nums)
            type_ = child_objs[0].type_string
            contains = \
                _('Contains {type:s} {indexlist:s}').format(type=type_,
                                                            indexlist=nums)
            self.set_tooltip_text(contains)

    @GObject.property(type=float, default=0.0, minimum=0.0, maximum=100.0)
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, value):
        self._usage = value

    @property
    def hwloc_object(self):
        return self.__hwloc_obj

    @property
    def is_partially_selected(self):
        return self._check_button.get_inconsistent()

    @property
    def is_selected(self):
        assert not self.is_partially_selected
        return self._check_button.get_active()

    @is_selected.setter
    def is_selected(self, is_set):
        self._check_button.set_inconsistent(False)
        self._check_button.set_active(is_set)

    def set_selection_mode(self, mode):
        self._check_button.set_sensitive(mode)

    def _check_button_toggled(self, button):
        button.set_inconsistent(False)
        _TopologyCPUView.Checkbox_Changed.emit_signal()

    def update_bitmap_selection(self, bitmap):
        if self.hwloc_object.complete_cpuset in bitmap:
            self.is_selected = True
        else:
            self.is_selected = False
            if bitmap.intersects(self.hwloc_object.complete_cpuset):
                self._check_button.set_inconsistent(True)
        for offs in self.offspring:
            offs.update_bitmap_selection(bitmap)

    def update_usage(self):
        usage = 0.0
        for offs in self.offspring:
            usage += offs.update_usage()
        try:
            self.usage = usage / len(self.offspring)
        except ZeroDivisionError:
            pass
        return self.usage


class _PUView(_ObjectView):

    def __init__(self, obj, listbox, parent):
        super(_PUView, self).__init__(obj, listbox, parent)

    def update_usage(self):
        try:
            self.usage = float(
                _TopologyCPUView.CPUStats[self.hwloc_object.os_index + 1].usage)
        except:
            self.usage = 0.0
        return self.usage

_SystemView = _ObjectView
_MachineView = _ObjectView
_NodeView = _ObjectView
_SocketView = _ObjectView
_CacheView = _ObjectView
_CoreView = _ObjectView
_GroupView = _ObjectView
_MiscView = _ObjectView

_VIEWS_BY_TYPE = {hwloc.OBJ_SYSTEM: _SystemView,
                  hwloc.OBJ_MACHINE: _MachineView,
                  hwloc.OBJ_NODE: _NodeView,
                  hwloc.OBJ_SOCKET: _SocketView,
                  hwloc.OBJ_CACHE: _CacheView,
                  hwloc.OBJ_CORE: _CoreView,
                  hwloc.OBJ_PU: _PUView,
                  hwloc.OBJ_GROUP: _GroupView,
                  hwloc.OBJ_MISC: _MiscView, }


def _type_view(obj, listbox, parent):
    cls = _VIEWS_BY_TYPE[obj.type]
    return cls(obj, listbox, parent)


class CPUSelectionLabel(Gtk.Label):

    def __init__(self, *args, **kwargs):
        super(CPUSelectionLabel, self).__init__(self, name='smallLabel',
                                                single_line_mode=True,
                                                track_visited_links=False,
                                                *args, **kwargs)
        self._selection_string = ''
        self._dropped_text = ''

    @GObject.property(str, '')
    def selection_string(self):
        return self._selection_string

    @selection_string.setter
    def selection_string(self, value):
        self._selection_string = value
        self.set_text(_('CPU Selection: ') + value)


class _WorkArea(Gtk.ButtonBox):

    def __init__(self):
        super(_WorkArea, self).__init__(visible=True, layout_style='start')
        self._selection_mode = False
        self._selection_changed = False
        self.accept_button = Gtk.Button(visible=True, label='OK')
        self.bind_property('selection-mode', self.accept_button, 'sensitive',
                           GObject.BindingFlags.INVERT_BOOLEAN)
        self.bind_property('selection-changed', self.accept_button,
                           'sensitive')
        self.add(self.accept_button)
        self.set_child_non_homogeneous(self.accept_button, True)
        self.select_all_button = Gtk.Button(visible=True, label='All')
        self.add(self.select_all_button)
        self.set_child_non_homogeneous(self.select_all_button, True)
        self.set_child_secondary(self.select_all_button, True)
        self.unselect_all_button = Gtk.Button(visible=True,
                                              label='None')
        self.add(self.unselect_all_button)
        self.set_child_secondary(self.unselect_all_button, True)
        self.set_child_non_homogeneous(self.unselect_all_button, True)

    @GObject.property(type=bool, default=False)
    def selection_changed(self):
        return self._selection_changed

    @selection_changed.setter
    def selection_changed(self, value):
        self._selection_changed = value
        ctx = self.accept_button.get_style_context()
        if value:
            ctx.add_class('suggested-action')
        else:
            ctx.remove_class('suggested-action')
        self.accept_button.set_sensitive(value)

    @GObject.property(type=bool, default=False)
    def selection_mode(self):
        return self._selection_mode

    @selection_mode.setter
    def selection_mode(self, value):
        self._selection_mode = value
        self.selection_changed = False


class _TopologyHeaderBar(Gtk.HeaderBar):

    def __init__(self):
        super(_TopologyHeaderBar, self).__init__(visible=True,
                                                 show_close_button=False,
                                                 expand=False, valign='start')
        self.set_custom_title(Gtk.Label(_('Topology'), name='titleLabel',
                                        visible=True))
        self._selection_mode = False
        self._selection_changed = False
        self._at_toplevel = True
        if Gtk.check_version(3, 12, 0) is None:
            self.set_has_subtitle(False)
        self.back_button = Gtk.Button(visible=False, no_show_all=True,
                                      expand=False, valign='center',
                                      relief='none')
        self.cancel_button = Gtk.Button(visible=False, no_show_all=True,
                                        focus_on_click=False, expand=False,
                                        valign='center')
        if Gtk.Widget.get_default_direction() != Gtk.TextDirection.RTL:
            pname = 'go-previous-symbolic'
            uname = 'edit-undo-symbolic'
        else:
            pname = 'go-previous-rtl-symbolic'
            uname = 'edit-undo-rtl-symbolic'
        self.back_button.set_image(Gtk.Image(icon_name=pname,
                                             icon_size=Gtk.IconSize.MENU))
        self.cancel_button.set_image(Gtk.Image(icon_name=uname,
                                               icon_size=Gtk.IconSize.MENU))
        self.pack_start(self.back_button)
        flags = GObject.BindingFlags.INVERT_BOOLEAN | GObject.BindingFlags.SYNC_CREATE
        self.bind_property('at-toplevel', self.back_button, 'visible', flags)
        self.selection_mode_button = Gtk.Button(visible=True,
                                                focus_on_click=False,
                                                expand=False, valign='center',
                                                relief='none')
        img = Gtk.Image(icon_name='object-select-symbolic',
                        icon_size=Gtk.IconSize.MENU)
        self.selection_mode_button.set_image(img)
        self.pack_end(self.selection_mode_button)
        self.pack_end(self.cancel_button)
        self.bind_property('selection-mode', self.selection_mode_button, 'visible',
                           GObject.BindingFlags.INVERT_BOOLEAN)
        self.connect('notify::selection-mode',
                     self._on_notify_selection_mode)
        self.bind_property('selection-mode', self.cancel_button, 'visible')

    def _on_notify_selection_mode(self, _widget, _parameter):
        if not self.selection_mode:
            self.back_button.set_property('visible', not self.at_toplevel)
        else:
            self.back_button.hide()

    @GObject.property(type=bool, default=True)
    def at_toplevel(self):
        return self._at_toplevel

    @at_toplevel.setter
    def at_toplevel(self, value):
        self._at_toplevel = value

    @GObject.property(type=bool, default=False)
    def selection_mode(self):
        return self._selection_mode

    @selection_mode.setter
    def selection_mode(self, value):
        self._selection_mode = value
        self.selection_changed = False

    @GObject.property(type=bool, default=False)
    def selection_changed(self):
        return self._selection_changed

    @selection_changed.setter
    def selection_changed(self, value):
        ctx = self.cancel_button.get_style_context()
        if value:
            ctx.add_class('destructive-action')
        else:
            ctx.remove_class('destructive-action')


class _TopologyCPUView(Gtk.Grid):
    Checkbox_Changed = Signaler('CheckboxChanged')
    CPUStats = procfs.cpusstats()

    def __init__(self):
        self._selection_mode = False
        self._selection_changed = False
        self._at_toplevel = True
        self._usage = 0
        super(_TopologyCPUView, self).__init__(orientation='vertical',
                                               row_homogeneous=False,
                                               column_homogeneous=False,
                                               row_spacing=3, visible=True,
                                               expand=True, halign='fill')
        header_bar = _TopologyHeaderBar()
        header_bar.back_button.connect('clicked',
                                       self._back_button_clicked)
        header_bar.selection_mode_button.connect('clicked',
                                                 self._selection_mode_button_clicked)
        header_bar.cancel_button.connect('clicked',
                                         self._cancel_button_clicked)
        self.add(header_bar)
        self._list_box = Gtk.ListBox(visible=True,
                                     activate_on_single_click=True,
                                     selection_mode='none', expand=True,
                                     halign='fill', valign='fill')
        self._showlist = None
        self.selected_bitmap = AffinityBitmap(Topology.complete_cpuset)
        self._saved_bitmap = None
        self._selection_text = CPUSelectionLabel(visible=True,
                                                 hexpand=True,
                                                 valign='end',
                                                 halign='start')
        self.bind_property('selection-string', self._selection_text,
                           'selection-string',
                           GObject.BindingFlags.SYNC_CREATE)
        self.bind_property('selection-mode', self._selection_text,
                           'visible',
                           GObject.BindingFlags.INVERT_BOOLEAN)
        self.bind_property('selection-mode',
                           header_bar, 'selection-mode',
                           GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property('selection-changed',
                           header_bar, 'selection-changed',
                           GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property('at-toplevel', header_bar,
                           'at-toplevel')
        scrolled_window = Gtk.ScrolledWindow(visible=True,
                                             hscrollbar_policy='never',
                                             expand=True, valign='fill',
                                             halign='fill')
        scrolled_window.add(self._list_box)
        self.add(scrolled_window)
        self.add(self._selection_text)
        self._button_box = _WorkArea()
        self._button_box.accept_button.connect('clicked',
                                               self._accept_button_clicked)
        self._button_box.select_all_button.connect('clicked',
                                                   self._select_all_button_clicked)
        self._button_box.unselect_all_button.connect('clicked',
                                                     self._unselect_all_button_clicked)
        revealer = Gtk.Revealer(visible=True, transition_type='slide-up',
                                expand=False, valign='end', halign='start')
        revealer.add(self._button_box)
        self.add(revealer)
        self.bind_property('selection-mode',
                           self._button_box, 'selection-mode')
        self.bind_property('selection-changed',
                           self._button_box, 'selection-changed')
        self.bind_property('selection-mode', revealer, 'reveal-child')
        self._displayed_depth = Topology.depth
        self._toplevel_obj = Topology.root_obj
        self._toplevel_view = _type_view(self._toplevel_obj, self._list_box,
                                         None)
        self._toplevel_view.update_bitmap_selection(self.selected_bitmap)
        self._view_above_current = self._toplevel_view
        self._displayed_depth = \
            self._toplevel_view.offspring[0].hwloc_object.depth
        self._list_box.set_filter_func(self._list_filter, None)
        self._list_box.connect('row-activated', self._list_row_activated)
        self._list_box.invalidate_filter()
        self._list_box.set_header_func(self._header_func, None)
        self._list_box.invalidate_headers()
        self.Checkbox_Changed.connect_handler(self._checkbox_changed)

        def _preload_cpusstats():
            self.CPUStats.reload()  # I/O happens here
        threading.Thread(target=_preload_cpusstats).start()

    def refresh(self):
        def _update_usage():
            self.usage = self._toplevel_view.update_usage()
            return False

        def _reload_cpusstats():
            self.CPUStats.reload()  # I/O happens here
            # don't change the GUI outside the GTK main loop
            GLib.idle_add(_update_usage)
        # start a Python thread and let the main loop continue
        threading.Thread(target=_reload_cpusstats).start()

    @GObject.property(type=bool, default=True)
    def at_toplevel(self):
        return self._at_toplevel

    @at_toplevel.setter
    def at_toplevel(self, value):
        self._at_toplevel = value

    @GObject.property(type=bool, default=False)
    def selection_mode(self):
        return self._selection_mode

    @selection_mode.setter
    def selection_mode(self, value):
        self._selection_mode = value
        self.selection_changed = False

    @GObject.property(type=bool, default=False)
    def selection_changed(self):
        return self._selection_changed

    @selection_changed.setter
    def selection_changed(self, value):
        self._selection_changed = value

    @GObject.property(type=float, default=0.0, minimum=0.0, maximum=100.0)
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, value):
        self._usage = value

    @GObject.property(str, '')
    def selection_string(self):
        return self.selected_bitmap.get_friendly_text()

    @selection_string.setter
    def selection_string(self, value):
        pass

    def _back_button_clicked(self, _):
        self.go_back()

    def _selection_mode_button_clicked(self, _):
        self.start_selection_mode()

    def _cancel_button_clicked(self, _):
        self.cancel_selection_mode()

    def _checkbox_changed(self, _):
        if not self._showlist:
            return
        for view in self._showlist:
            if not view.is_partially_selected:
                if not view.is_selected:
                    self.selected_bitmap &= ~view.hwloc_object.complete_cpuset
                else:
                    self.selected_bitmap |= view.hwloc_object.complete_cpuset
        self.selection_string = self.selected_bitmap.get_friendly_text()
        self.selection_changed = True

    def _header_func(self, row, before, _):
        if before is None:
            row.set_header(Gtk.Label(_header_string(row.get_child().parent.hwloc_object),
                                     name='smallGrayLabel', use_markup=True,
                                     visible=True))

    def _set_selection_mode(self, mode):
        self.selection_mode = mode
        for view in self._showlist:
            view.set_selection_mode(mode)
        if not mode:
            self._showlist = None

    def cancel_selection_mode(self):
        self._set_selection_mode(False)
        self.selected_bitmap = AffinityBitmap(self._saved_bitmap)
        self.selection_string = self.selected_bitmap.get_friendly_text()
        self._view_above_current.update_bitmap_selection(self.selected_bitmap)

    def start_selection_mode(self):
        self._saved_bitmap = self.selected_bitmap.dup()
        self._showlist = []
        self._list_box.invalidate_filter()
        self._set_selection_mode(True)

    def _accept_button_clicked(self, _):
        self._toplevel_view.update_bitmap_selection(self.selected_bitmap)
        self._set_selection_mode(False)

    def _select_all_button_clicked(self, _):
        for offs in self._view_above_current.offspring:
            offs.is_selected = True

    def _unselect_all_button_clicked(self, _):
        for offs in self._view_above_current.offspring:
            offs.is_selected = False

    def _check_toplevel(self):
        self.at_toplevel = \
            self._displayed_depth == self._toplevel_obj.first_child.depth

    def go_back(self):
        self._view_above_current = self._view_above_current.parent
        obj = self._view_above_current.hwloc_object
        self._displayed_depth = obj.first_child.depth
        self._check_toplevel()
        self._list_box.invalidate_filter()

    def _list_filter(self, row, _):
        view = row.get_child()
        visible = view in self._view_above_current.offspring
        if visible and self._showlist is not None:
            self._showlist.append(view)
        return visible

    def _list_row_activated(self, _widget, row):
        if self.selection_mode:
            return
        view = row.get_child()
        child = view.hwloc_object.first_child
        if not child:
            return
        self._displayed_depth = child.depth
        self._view_above_current = view
        self._list_box.invalidate_filter()
        self._check_toplevel()


class _AppHeaderBar(Gtk.HeaderBar):

    def __init__(self):
        super(_AppHeaderBar, self).__init__(visible=True,
                                            title=_('System View'),
                                            show_close_button=False,
                                            expand=False)
        if Gtk.check_version(3, 12, 0) is None:
            self.set_has_subtitle(False)
        self.hide_button = Gtk.Button(visible=True, expand=False,
                                      valign='center')
        self.hide_button.set_image(Gtk.Image(icon_name='window-close-symbolic',
                                             icon_size=Gtk.IconSize.MENU))
        self.pack_end(self.hide_button)


class SelectionWindow(Gtk.ApplicationWindow):

    def __init__(self):
        super(SelectionWindow, self).__init__(title=_('CPU selection'),
                                              show_menubar=False,
                                              deletable=False,
                                              default_height=500,
                                              default_width=800)
        self._usage = 0.0
        self._selection_string = ''
        header_bar = _AppHeaderBar()
        header_bar.hide_button.connect('clicked', self._hide_button_clicked)
        self.set_titlebar(header_bar)
        self._pciview = PCIView(margin=1, hexpand=True)
        scrolled_window = Gtk.ScrolledWindow(visible=True,
                                             vscrollbar_policy='automatic',
                                             hscrollbar_policy='never')
        scrolled_window.add(self._pciview)
        if Topology.complete_cpuset is None:
            text = _('Pianofish can only operate on the topology of a single system')
            text2 = _('The application will now exit')
            errdialog = Gtk.MessageDialog(parent=self.get_toplevel(),
                                          title='pianofish',
                                          text=text,
                                          secondary_text=text2,
                                          buttons=Gtk.ButtonsType.CLOSE)
            errdialog.run()
            errdialog.destroy()
            raise AppQuitException
        self._topology_view = _TopologyCPUView()
        self._topology_view.bind_property('usage', self, 'usage')
        self._topology_view.bind_property('selection-string', self,
                                          'selection-string',
                                          GObject.BindingFlags.SYNC_CREATE)
        grid = Gtk.Grid(visible=True, orientation='horizontal',
                        column_spacing=4,
                        row_homogeneous=True, column_homogeneous=False)
        grid.add(self._topology_view)
        grid.add(scrolled_window)
        self.add(grid)

    @GObject.property(type=float, default=0.0, minimum=0.0, maximum=100.0)
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, value):
        self._usage = value

    @GObject.property(str, '')
    def selection_string(self):
        return self._selection_string

    @selection_string.setter
    def selection_string(self, value):
        self._selection_string = value
        self._pciview.update_selection(self._topology_view.selected_bitmap)

    def refresh(self):
        self._topology_view.refresh()

    def _hide_button_clicked(self, _):
        self.hide()
