#!/usr/bin/env python2
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
import sys

# TODO: for testing only
try:
    os.environ['GSETTINGS_SCHEMA_DIR'] = os.environ['PWD']
except KeyError:
    pass

from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Gio, GLib, GObject

from pianofish import translation
from pianofish.utilities import Signaler, LockButton, Settings, AppQuitSignal,\
    AppQuitException
from pianofish.systemview import SelectionWindow, UsageLevelBar,\
    CPUSelectionLabel
from pianofish.irqview import IRQView
from pianofish.processview import ProcessView

_Version = '1.0'
_Package_name = 'pianofish'
_Author = 'Guy Streeter'
_Author_email = '<guy.streeter@gmail.com>'
_License = 'GPLv2+'
_Description = 'pianofish is not (quite) tuna'

class _AboutPianofish(Gtk.AboutDialog):
    def __init__(self, parent):
        super(_AboutPianofish, self).__init__(parent=parent,
                                              title='About pianofish',
                                              authors=(_Author,),
                                              copyright='2015-2017 Red Hat, Inc.',
                                              license=_License,
                                              license_type=Gtk.License.GPL_2_0,
                                              version=_Version)

class _SelectionButton(Gtk.Button):

    def __init__(self, *args, **kwargs):
        super(_SelectionButton, self).__init__(*args, **kwargs)
        self._dopped_text = ''
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.drag_dest_add_text_targets()

    def do_drag_data_received(self, _context, _x, _y, data, _info, _time):
        self.dropped_text = data.get_text()

    @GObject.property(str, '')
    def dropped_text(self):
        return self._dopped_text

    @dropped_text.setter
    def dropped_text(self, value):
        self._dopped_text = value

_SettingsSignal = Signaler('SettingsClicked')


class _TopologyHeaderBar(Gtk.HeaderBar):

    def __init__(self):
        super(_TopologyHeaderBar, self).__init__(visible=True,
                                                 title='Pianofish',
                                                 show_close_button=True)
        if Gtk.check_version(3, 12, 0) is None:
            self.set_has_subtitle(False)
        self._usage = 0.0
        self._selection_string = ''
        self._dropped_text = ''
        self._filter_mode = False
        self._selection_window = SelectionWindow()
        self._selection_window.bind_property('usage', self, 'usage')
        self._selection_window.bind_property('selection-string', self,
                                             'selection-string',
                                             GObject.BindingFlags.SYNC_CREATE)
        lb = UsageLevelBar(visible=True, valign='fill', expand=True)
        sl = CPUSelectionLabel(visible=True, valign='center',
                               expand=False)
        self.bind_property('usage', lb, 'usage')
        self.bind_property('selection-string', sl, 'selection-string',
                           GObject.BindingFlags.SYNC_CREATE)
        self._selection_button = _SelectionButton(visible=True,
                                                  vexpand=False)
        self._selection_button.add(sl)
        self._selection_button.connect('clicked',
                                       self._selection_button_clicked)
        self._selection_button.bind_property('dropped-text', self,
                                             'dropped-text',
                                             GObject.BindingFlags.DEFAULT)
        self.pack_start(lb)
        self.pack_start(self._selection_button)
        lock_button = LockButton()
        self.pack_end(lock_button)
        img = Gtk.Image(icon_name='emblem-system-symbolic', visible=True,
                        icon_size=1)
        button = Gtk.Button(visible=True, image=img, expand=False,
                            focus_on_click=False, valign='center',
                            relief='none')
        button.connect('clicked', self._settings_button_clicked)
        self.pack_end(button)
        toggle = Gtk.ToggleButton(visible=True, focus_on_click=False,
                                  expand=False, valign='center',
                                  relief='none')
        toggle.set_property('tooltip-text', _('Filter process list'))
        img = Gtk.Image(icon_name='edit-select-symbolic',
                        icon_size=Gtk.IconSize.MENU)
        toggle.set_image(img)
        toggle.set_active(False)
        toggle.bind_property('active', self, 'filter-mode',
                             GObject.BindingFlags.BIDIRECTIONAL)
        self.pack_end(toggle)

    @GObject.property(type=bool, default=False)
    def filter_mode(self):
        return self._filter_mode

    @filter_mode.setter
    def filter_mode(self, value):
        self._filter_mode = value

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

    @GObject.property(str, '')
    def dropped_text(self):
        return self._dropped_text

    @dropped_text.setter
    def dropped_text(self, value):
        self._dropped_text = value

    def refresh(self):
        self._selection_window.refresh()

    def _selection_button_clicked(self, _):
        self._selection_window.present()

    def _settings_button_clicked(self, _):
        _SettingsSignal.emit_signal()


class _MainPane(Gtk.Paned):

    def __init__(self):
        super(_MainPane, self).__init__(visible=True, orientation='vertical',
                                        border_width=3)
        self._filter_mode = False
        self._drop_destination = {}
        scrolled_window = Gtk.ScrolledWindow(visible=True,
                                             vscrollbar_policy='automatic',
                                             hscrollbar_policy='never',
                                             shadow_type='in')
        self.irq_view = IRQView(expand=True, margin=2)
        self._drop_destination['irq'] = self.irq_view
        scrolled_window.add(self.irq_view)
        self.pack1(scrolled_window, resize=True, shrink=True)
        self.process_view = ProcessView(expand=True,
                                        margin_top=2)
        self.bind_property('filter-mode', self.process_view,
                           'filter-mode', GObject.BindingFlags.DEFAULT)
        self._drop_destination['process'] = self.process_view
        self.pack2(self.process_view, resize=True, shrink=True)

    def refresh(self, cpu_selection):
        self.irq_view.refresh(cpu_selection)
        self.process_view.refresh(cpu_selection)

    def settings_changed(self):
        self.irq_view.settings_changed()
        self.process_view.settings_changed()

    def handle_dropped_text(self, text, cpu_selection):
        try:
            dest, text = text.split(':', 1)
            handler = self._drop_destination[dest]
        except ValueError:
            return
        except KeyError:
            return
        handler.handle_dropped_text(text, cpu_selection)

    @GObject.property(type=bool, default=False)
    def filter_mode(self):
        return self._filter_mode

    @filter_mode.setter
    def filter_mode(self, value):
        self._filter_mode = value


class _Win(Gtk.ApplicationWindow):

    def __init__(self):
        super(_Win, self).__init__(title='pianofish', show_menubar=False,
                                   default_height=800, default_width=1000)
        # This affects the name shown on the application menu
        self.set_wmclass('Pianofish', 'Pianofish')
        for f in ['.', os.path.dirname(__file__), '/usr/share/pianofish']:
            try:
                self.set_icon_from_file(os.path.join(f, 'pianofish.svg'))
                # The About dialog uses this:
                self.set_default_icon_from_file(os.path.join(f, 'pianofish.svg'))
                break
            except GLib.Error:
                continue
        csstext = b"""
        GtkLabel#smallLabel {
            font-size: smaller;
        }
        GtkLabel#smallGrayLabel {
            font-size: smaller;
            background-color: shade(@theme_bg_color, 0.8);
        }
        GtkLabel#titleLabel {
            font-size: smaller;
            font-weight: bold;
        }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(csstext)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                                 css_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self._headerbar = _TopologyHeaderBar()
        self.set_titlebar(self._headerbar)
        self._headerbar.connect('notify::dropped-text',
                                self.on_notify_headerbar_dropped_text)
        self._pane = _MainPane()
        self._headerbar.bind_property('filter-mode', self._pane,
                                      'filter-mode',
                                      GObject.BindingFlags.DEFAULT)
        self._headerbar.connect('notify::filter-mode',
                                self._on_notify_headerbar_filter_mode)
        self.add(self._pane)
        action = Gio.SimpleAction.new_stateful('use-filter', None,
                                               GLib.Variant('b', False))
        action.connect('change-state', self._filter_state_changed)
        self.add_action(action)
        self._filter_action = action
        self.refresh()

    def _filter_state_changed(self, action, value):
        self._headerbar.filter_mode = value
        action.set_state(value)

    def refresh(self):
        self._pane.refresh(self._headerbar.selection_string)
        self._headerbar.refresh()

    def settings_changed(self):
        self._pane.settings_changed()

    def on_notify_headerbar_dropped_text(self, headerbar, _):
        self._pane.handle_dropped_text(headerbar.dropped_text,
                                       headerbar.selection_string)

    def _on_notify_headerbar_filter_mode(self, _headerbar, param):
        self._filter_action.set_state(GLib.Variant('b', bool(param)))


class _AppPreferences(Gtk.Dialog):

    def __init__(self, parent):
        super(_AppPreferences, self).__init__(parent=parent,
                                              title=_('Preferences'))
        action_grid = Gtk.Grid(visible=True, margin=8, row_spacing=8,
                               orientation='vertical')
        spinner_grid = Gtk.Grid(visible=True, orientation='horizontal',
                                column_homogeneous=False,
                                column_spacing=3,
                                border_width=3, halign='center')
        adjustment = Gtk.Adjustment(0, 2, 9999, 1, 5, 0)
        spin_button = Gtk.SpinButton(visible=True, numeric=True,
                                     adjustment=adjustment)
        Settings.bind('interval', spin_button, 'value',
                      Gio.SettingsBindFlags.DEFAULT)
        label = Gtk.Label(visible=True, label=_('Update _interval:'),
                          use_underline=True, margin_end=2)
        label.set_mnemonic_widget(spin_button)
        spinner_grid.add(label)
        spinner_grid.add(spin_button)
        action_grid.add(spinner_grid)
        glob_grid = Gtk.Grid(visible=True, row_spacing=0,
                             margin_start=0,
                             margin_top=4, margin_bottom=8,
                             orientation='vertical')
        glob_grid.add(Gtk.Label(visible=True,
                                halign='start',
                                label=_('Process filter method:')))
        self._glob_button = Gtk.RadioButton(visible=True, margin_start=16,
                                            use_underline=True,
                                            label=_('Bash-style _glob'))
        glob_grid.add(self._glob_button)
        self._regex_button = Gtk.RadioButton(group=self._glob_button,
                                             visible=True, margin_start=16,
                                             use_underline=True,
                                             label=_('_Regular expression'))
        glob_grid.add(self._regex_button)
        action_grid.add(glob_grid)
        Settings.bind('glob', self._glob_button, 'active',
                      Gio.SettingsBindFlags.DEFAULT)
        Settings.bind('glob', self._regex_button, 'active',
                      Gio.SettingsBindFlags.INVERT_BOOLEAN)
        self._kernel_button = Gtk.CheckButton(visible=True,
                                              use_underline=True,
                                              label=_('Show _kernel threads'))
        action_grid.add(self._kernel_button)
        Settings.bind('kthreads', self._kernel_button, 'active',
                      Gio.SettingsBindFlags.DEFAULT)
        self._user_button = Gtk.CheckButton(visible=True,
                                            use_underline=True,
                                            label=_('Show _user threads'))
        action_grid.add(self._user_button)
        Settings.bind('uthreads', self._user_button, 'active',
                      Gio.SettingsBindFlags.DEFAULT)
        button = Gtk.CheckButton(visible=True, use_underline=True,
                                 label=_('Show thread _cgroups'))
        Settings.bind('cgroups', button, 'active',
                      Gio.SettingsBindFlags.DEFAULT)
        action_grid.add(button)
        self.get_content_area().add(action_grid)
        button = Gtk.Button(visible=True, label=_('_Close'),
                            use_underline=True)
        self.add_action_widget(button, Gtk.ResponseType.CLOSE)
        button.connect('clicked', self._close_button_clicked)

    def _close_button_clicked(self, _button):
        self.destroy()


class _AppMenu(Gio.Menu):

    def __init__(self):
        super(_AppMenu, self).__init__()
        item = Gio.MenuItem.new(_('_Filter processes'), 'win.use-filter')
        item.set_attribute_value('accel', GLib.Variant('s', _('<Ctrl>F')))
        menu = Gio.Menu()
        menu.append_item(item)
        self.append_section(None, menu)
        self.append(_('_Preferences'), 'app.preferences')
        self.append(_('_About'), 'app.about')
        item = Gio.MenuItem.new(_('_Quit'), 'app.quit')
        item.set_attribute_value('accel', GLib.Variant('s', _('<Ctrl>Q')))
        menu = Gio.Menu()
        menu.append_item(item)
        self.append_section(None, menu)


class _App(Gtk.Application):

    def __init__(self):
        global _SettingsSignal, AppQuitSignal
        flags = Gio.ApplicationFlags.NON_UNIQUE | Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        super(_App, self).__init__(application_id='org.fedora.pianofish',
                                   flags=flags)
        GLib.set_application_name('Pianofish')
        GLib.set_prgname('Pianofish')
        self._win = None
        self._args = None
        self._interval_id = None
        self._update_interval = 0
        _SettingsSignal.connect_handler(self._preferences_activated)
        AppQuitSignal.connect_handler(self._quit_activated)

    def do_command_line(self, commandline):
        Gtk.Application.do_command_line(self, commandline)
        self.do_activate()
        return 0

    def _preferences_activated(self, *_args):
        _AppPreferences(self.get_active_window()).run()
        self._update_settings()

    def _about_activated(self, *_args):
        about = _AboutPianofish(self.get_active_window())
        about.run()
        about.destroy()

    def _refresh(self):
        self._win.refresh()
        return True

    def _update_settings(self):
        interval = Settings.get_int('interval')
        if self._interval_id is not None and interval != self._update_interval:
            GObject.source_remove(self._interval_id)
            self._interval_id = None
            if interval != 0:
                self._interval_id = GObject.timeout_add_seconds(interval,
                                                                self._refresh)
        self._update_interval = interval
        self._win.settings_changed()

    def _quit_activated(self, *_args):
        self.quit()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.set_app_menu(_AppMenu())
        simple_action = Gio.SimpleAction(name='preferences')
        simple_action.connect('activate', self._preferences_activated)
        self.add_action(simple_action)
        simple_action = Gio.SimpleAction(name='about')
        simple_action.connect('activate', self._about_activated)
        self.add_action(simple_action)
        simple_action = Gio.SimpleAction(name='quit')
        simple_action.connect('activate', self._quit_activated)
        self.add_action(simple_action)

    def do_activate(self):
        try:
            if self._win:
                self._win.present()
                return
            self._win = _Win()
            self._update_settings()
            self.add_window(self._win)
            self._win.present()
            self._interval_id = GObject.timeout_add_seconds(self._update_interval,
                                                            self._refresh)
        except AppQuitException:
            self.quit()


def run():
    sys.exit(_App().run(sys.argv))

if __name__ == '__main__':
    run()
