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

from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')

from gi.repository import GObject, GLib, Gtk, Gdk

import re
import threading

# When running with Python 3, import our own ethtool substitute.
try:
    import ethtool
except:
    from pianofish import ethtool

from pianofish.utilities import PIDStats, Interrupts,\
    RowItem, WeightedTextRow, WeightedTextTreeView,\
    WeightedTextListStore, PolicyChooser, PriorityChooser,\
    AffinityChooser, AttributesDialog, AdminProxy, set_text_drag_icon
from pianofish.bitmap import AffinityBitmap

import schedutils


class _IRQAttributesDialog(AttributesDialog):

    def __init__(self, parent, values, columns):
        title = _('Set IRQ Attributes')
        super(_IRQAttributesDialog, self).__init__(parent=parent,
                                                   title=title)
        main_grid = Gtk.Grid(visible=True, orientation='vertical',
                             expand=True,
                             row_spacing=10, border_width=5,
                             margin_top=5, margin_bottom=5)
        selection_grid = Gtk.Grid(visible=True, column_homogeneous=False,
                                  expand=True,
                                  orientation='horizontal',
                                  column_spacing=15)
        try:
            self._priority = values[columns['PRIORITY']]
        except:
            self._priority = -1
        if self._priority != -1:
            self._policy = values[columns['POLICY']]
            params = {'IRQ': values[columns['IRQ']],
                      'PID': values[columns['PID']],
                      'user': values[columns['USERS']]}
            label = _('IRQ {IRQ:d} (PID {PID:d}): {user:s}').format(**params)
            self._priority_chooser = PriorityChooser(self._priority,
                                                     expand=True)
            self._priority_chooser.bind_property('selected_priority', self,
                                                 'priority')
            self._priority_chooser.conditionally_enable('SCHED_' + self._policy)
            self._policy_chooser = PolicyChooser(self._policy,
                                                 expand=True)
            self._policy_chooser.bind_property('selected_policy', self,
                                               'policy',
                                               GObject.BindingFlags.SYNC_CREATE)
            selection_grid.add(self._policy_chooser)
            selection_grid.add(self._priority_chooser)
        else:
            self._policy = -1
            params = {'IRQ': values[columns['IRQ']],
                      'user': values[columns['USERS']]}
            label = _('IRQ {IRQ:d}: {user:s}').format(**params)
            self._policy_chooser = None
            self._priority_chooser = None
        affinity = AffinityBitmap(values[columns['AFFINITY']])
        self._affinity = affinity.get_friendly_text()
        self._affinity_chooser = AffinityChooser(self._affinity,
                                                 expand=True)
        self._affinity_chooser.bind_property('selected_affinity', self,
                                             'affinity')
        selection_grid.add(self._affinity_chooser)
        label = Gtk.Label(label=label, visible=True, expand=True,
                          margin=5, halign='fill')
        main_grid.add(label)
        label = _('<i>Only checked attributes will be changed</i>')
        label = Gtk.Label(label=label, visible=True, halign='fill',
                          valign='end', use_markup=True,
                          margin_left=5, margin_right=5,
                          margin_bottom=5, margin_top=10)
        main_grid.add(label)
        main_grid.add(selection_grid)
        self.get_content_area().add(main_grid)

    @GObject.property(str, '')
    def policy(self):
        return self._policy

    @policy.setter
    def policy(self, value):
        self._policy = value
        self._priority_chooser.conditionally_enable(value)

    @GObject.property(int, -1)
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @GObject.property(str, '')
    def affinity(self):
        return self._affinity

    @affinity.setter
    def affinity(self, value):
        self._affinity = value


class _ThreadViewRow(WeightedTextRow):
    def __init__(self):
        columns = (RowItem(_('IRQ'), 'IRQ', int),
                   RowItem(_('PID'), 'PID', int),
                   RowItem(_('Policy'), 'POLICY', str),
                   RowItem(_('Priority'), 'PRIORITY', int),
                   RowItem(_('Affinity'), 'AFFINITY', str),
                   RowItem(_('Events'), 'EVENTS', int),
                   RowItem(_('Users'), 'USERS', str))
        super(_ThreadViewRow, self).__init__(columns)
        self.sort_column = self['IRQ']

    def new_values(self, irq, affinity, nics):
        new_values = [None] * self.nr_columns
        users = Interrupts.get_irq_users(irq, nics)
        irq_re = re.compile("(irq/%s-.+|IRQ-%s)" % (irq, irq))
        pids = PIDStats.find_by_regex(irq_re)
        if pids:
            pid = pids[0]
            prio = PIDStats.rt_priority(PIDStats.pidstats()[pid])
            sched = schedutils.schedstr(schedutils.get_scheduler(pid))[6:]
        else:
            pid = -1
            prio = -1
            sched = ''
        new_values[self['IRQ']] = irq
        new_values[self['PID']] = pid
        new_values[self['POLICY']] = sched
        new_values[self['PRIORITY']] = prio
        new_values[self['AFFINITY']] = affinity.get_friendly_text()
        new_values[self['EVENTS']] = Interrupts.events(irq)
        new_values[self['USERS']] = ','.join(users)
        return new_values


class _NoThreadViewRow(WeightedTextRow):
    def __init__(self):
        columns = (RowItem(_('IRQ'), 'IRQ', int),
                   RowItem(_('Affinity'), 'AFFINITY', str),
                   RowItem(_('Events'), 'EVENTS', int),
                   RowItem(_('Users'), 'USERS', str))
        super(_NoThreadViewRow, self).__init__(columns)
        self.sort_column = self['IRQ']

    def new_values(self, irq, affinity, nics):
        new_values = [None] * self.nr_columns
        users = Interrupts.get_irq_users(irq, nics)
        new_values[self['IRQ']] = irq
        new_values[self['AFFINITY']] = affinity.get_friendly_text()
        new_values[self['EVENTS']] = Interrupts.events(irq)
        new_values[self['USERS']] = ','.join(users)
        return new_values


class IRQView(WeightedTextTreeView):

    def __init__(self, **kwargs):
        self._row = _ThreadViewRow() \
            if PIDStats.has_threaded_irqs() \
            else _NoThreadViewRow()
        super(IRQView, self).__init__(self._row, visible=True, **kwargs)
        self._cpu_selection = None
        self._button_press_location = None
        self._refreshing = True
        self.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [],
                                      Gdk.DragAction.COPY)
        self.drag_source_add_text_targets()
        self.connect('drag-data-get', self._on_drag_data_get)
        self._nics = None
        self._tree_store = WeightedTextListStore(self._row)
        self.set_model(self._tree_store)
        self._popup_menu = Gtk.Menu(visible=True)
        menu_item = Gtk.MenuItem(label=_('_Set IRQ attributes'), visible=True,
                                 use_underline=True)
        menu_item.connect('activate', self._on_edit_activated)
        self._refresh_checkbox = Gtk.CheckMenuItem(label=_('_Refresh the IRQ list'),
                                                   visible=True,
                                                   use_underline=True)
        flags = GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE
        self.bind_property('refreshing', self._refresh_checkbox,
                           'active', flags)
        self._popup_menu.add(menu_item)
        self._popup_menu.add(self._refresh_checkbox)

    @GObject.property(type=bool, default=True)
    def refreshing(self):
        return self._refreshing

    @refreshing.setter
    def refreshing(self, value):
        self._refreshing = value

    def do_button_press_event(self, event):
        # Hold on to the latest button press location, for later use
        self._button_press_location = event.x, event.y
        if event.type == Gdk.EventType.BUTTON_PRESS \
                and event.button == Gdk.BUTTON_SECONDARY:
            self._popup_menu.popup(None, None, None, None, event.button,
                                   event.time)
            return True
        return WeightedTextTreeView.do_button_press_event(self, event)

    def _on_edit_activated(self, _widget):
        path = self.get_path_at_pos(self._button_press_location[0],
                                    self._button_press_location[1])[0]
        if not path:
            return
        iter_ = self._tree_store.get_iter(path)
        values = self._tree_store.get(iter_, *range(self._row.nr_columns))
        dialog = _IRQAttributesDialog(self.get_toplevel(), values, self._row)
        result = dialog.run()
        dialog.destroy()
        if result != Gtk.ResponseType.OK:
            return
        try:
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
        try:
            pid = values[self._row['PID']]
            policy = values[self._row['POLICY']]
            priority = values[self._row['PRIORITY']]
            new_policy = schedutils.schedfromstr(dialog.policy)
            # set policy and priority to -1 to leave them unchanged
            if policy == new_policy:
                policy = -1
            else:
                policy = new_policy
            if priority == dialog.priority:
                priority = -1
            else:
                priority = dialog.priority
        except KeyError:
            pid = -1
            policy = -1
            priority = -1
        # set affinity to empty string to leave it unchanged
        if new_affinity == AffinityBitmap(values[self._row['AFFINITY']]):
            new_affinity = ''
        else:
            new_affinity = str(new_affinity)
        # update_irqs() takes a list of IRQs and their settings, (a list of
        # lists) but we are not currently supporting multi-select in the IRQ
        # view
        irqs = ((values[self._row['IRQ']], pid, policy, priority, new_affinity),)
        AdminProxy.update_irqs(self._update_callback, irqs)

    def _update_callback(self, result):
        if result.succeeded:
            irq = str(result.successes[0])
            message = _('Attribute changes succeeded for IRQ {irq}')
            message = message.format(irq=irq)
        else:
            message = _('Failed to set attributes for IRQ:\n{reason}')
            message = message.format(reason=result.error_string)
        # a widget to show in the popover, with big margins all around
        label = Gtk.Label(label=message, visible=True, wrap=True,
                          margin_top=12, margin_bottom=12,
                          margin_start=5, margin_end=5)
        # popover positioned relative to the treeview
        popover = Gtk.Popover.new(self)
        popover.set_position(Gtk.PositionType.BOTTOM)
        # button press location is recorded relative to the enclosing
        # window
        rect = Gdk.Rectangle()
        rect.x = self._button_press_location[0]
        rect.y = self._button_press_location[1]
        rect.x, rect.y = self.convert_bin_window_to_widget_coords(rect.x,
                                                                  rect.y)
        popover.set_pointing_to(rect)
        popover.add(label)
        popover.show()
        # should always be true by the time this can run
        if self._cpu_selection is not None:
            # it would be better to just update the one IRQ we changed,
            # but if we changed its affinity, it might no longer be visible
            self.refresh(self._cpu_selection)

    def refresh(self, cpu_selection):
        if not self.refreshing:
            return
        self._cpu_selection = cpu_selection

        def _do_update():
            self._update_usage(cpu_selection)

        def _reload_interrupts():
            # These do I/O
            PIDStats.reload()
            Interrupts.reload(wait=True)
            self._nics = ethtool.get_active_devices()
            # Update the GUI in the main loop
            GLib.idle_add(_do_update)
        # Start a (Python) thread for I/O
        threading.Thread(target=_reload_interrupts).start()

    def settings_changed(self):
        # TODO: apply any global property changes to this widget
        pass

    def _update_usage(self, cpu_selection):
        selected_bitmap = AffinityBitmap(cpu_selection)
        # Build a list of the currents IRQ Numbers
        new_irqs = list(sorted(set(Interrupts.irqs())))
        # Walk the list store removing, adding, or updating IRQs
        row = self._tree_store.get_iter_first()
        while row:
            irq = self._tree_store.get_value(row, self._row['IRQ'])
            if irq not in new_irqs:
                if self._tree_store.remove(row):
                    # there is another row
                    continue
                # there are no more rows
                break
            affinity = Interrupts.affinity(irq)
            # TODO: show if any bits match, or only if all are included?
            # intersects() is true if any bits are the same.
            # if we want exact match, we could use "==" instead.
            # intersects() fails if affinity is empty (can't happen?)
            if not affinity.iszero and not affinity.intersects(selected_bitmap):
                new_irqs.remove(irq)
                if self._tree_store.remove(row):
                    continue
                break
            try:
                new_irqs.remove(irq)
                self._set_row_values(row, irq, affinity)
            except:
                if self._tree_store.remove(row):
                    continue
                break
            row = self._tree_store.iter_next(row)
        for irq in new_irqs:
            affinity = Interrupts.affinity(irq)
            if not affinity.iszero and not affinity.intersects(selected_bitmap):
                continue
            row = self._tree_store.append()
            try:
                self._set_row_values(row, irq, affinity)
            except:
                self._tree_store.remove(row)

    def handle_dropped_text(self, text, cpu_selection):
        # just so we know where the dropped text came from
        if text != 'set selection to bitmap':
            return
        selection = self.get_selection()
        affinity_string = str(AffinityBitmap(cpu_selection))

        irq_array = []
        def foreach_selected_get_values(model, _path, iter_, _data):
            irq = model.get_value(iter_, self._row['IRQ'])
            irq_array.append((irq, 0, -1, -1, affinity_string))

        # multi-select is not enabled, so this should just be one IRQ
        selection.selected_foreach(foreach_selected_get_values, None)
        AdminProxy.update_irqs(self._update_callback, irq_array)

    def _set_irq_affinity(self, irqthread, affinity):
        try:
            irqthread.set_affinity(affinity)
        except:
            kwargs = {'IRQ': irqthread.irq,
                      'affinity': affinity.get_friendly_text()
                     }
            text = _('Set affinity {affinity:s} for IRQ {IRQ:d} failed')
            text = text.format(**kwargs)
            text2 = _('No error information is available')
            dialog = Gtk.MessageDialog(parent=self.get_toplevel(),
                                       title='pianofish',
                                       text=text,
                                       secondary_text=text2,
                                       buttons=Gtk.ButtonsType.CLOSE)
            dialog.run()
            dialog.destroy()

    def _set_row_values(self, row, irq, affinity):
        new_values = self._row.new_values(irq, affinity, self._nics)
        self._tree_store.set_row_values(row, new_values)

    # the do_drag_data_get virtual method doesn't work right
    def _on_drag_data_get(self, _widget, _context, selection_data, _info,
                          _time):
        assert selection_data.set_text('irq:set selection to bitmap', -1)
        return True

# Doesn't work
#    def do_drag_data_get(self, context, selection_data, info, time):
#        assert selection_data.set_text('irq:set selection to bitmap', -1)

    def do_drag_begin(self, context):
        selection = self.get_selection()

        irqs = []
        def foreach_selected_cb(model, _path, iter_, irqs_):
            irqs_.append(str(model.get_value(iter_, self._row['IRQ'])))

        selection.selected_foreach(foreach_selected_cb, irqs)
        # create a drag icon containing the IRQ number
        string = 'IRQ: ' + ','.join(irqs)
        set_text_drag_icon(self, context, string)
        return True
