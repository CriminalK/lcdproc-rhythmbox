# -*- coding: utf-8 -*-

# Copyright (c) 2011 Nikolai Knopp <mike_rofone at imail.de>
# Was adapted from JamendoConfigureDialog.py
#
# Copyright (C) 2007 - Guillaume Desmottes
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import rb
from gi.repository import GObject
from gi.repository import PeasGtk
from gi.repository import RB
from gi.repository import Gio
from gi.repository import Gtk

class LCDProcPluginConfigureDialog (GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'LCDProcPluginConfig'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.lcdproc-plugin")

    def do_create_configure_widget(self):
        ui_file = rb.find_plugin_file(self, "lcdproc_config.ui")
        self.builder = Gtk.Builder()
        self.builder.add_from_file(ui_file)

        grid = self.builder.get_object("grid")

        entry_address = self.builder.get_object("entry_address")
        self.settings.bind("address", entry_address, "text", Gio.SettingsBindFlags.GET_NO_CHANGES)

        spinbutton_port = self.builder.get_object("spinbutton_port")
        self.settings.bind("port", spinbutton_port, "value", Gio.SettingsBindFlags.GET_NO_CHANGES)

        hscale_screenduration = self.builder.get_object("hscale_screenduration")
        self.settings.bind("screenduration", hscale_screenduration.props.adjustment, "value", Gio.SettingsBindFlags.GET_NO_CHANGES)

        self.hscale_scrollduration = self.builder.get_object("hscale_scrollduration")
        self.settings.bind("scrollduration", self.hscale_scrollduration.props.adjustment, "value", Gio.SettingsBindFlags.GET_NO_CHANGES)

        self.entry_scrollseparator = self.builder.get_object("entry_scrollseparator")
        self.settings.bind("scrollseparator", self.entry_scrollseparator, "text", Gio.SettingsBindFlags.GET_NO_CHANGES)

        comboboxtext_scrolling = self.builder.get_object("comboboxtext_scrolling")
        comboboxtext_scrolling.connect("changed", self.comboboxtext_scrolling_changed)
        comboboxtext_scrolling.set_active(self.settings.get_enum("scrolling"))

        return grid

    def comboboxtext_scrolling_changed(self, comboboxtext):
        scrolling = comboboxtext.get_active()
        self.settings.set_enum("scrolling", scrolling)

        if (self.settings.get_string("scrolling") == "Rolling"):
            self.hscale_scrollduration.set_sensitive(True)
            self.entry_scrollseparator.set_sensitive(True)
        else:
            self.hscale_scrollduration.set_sensitive(False)
            self.entry_scrollseparator.set_sensitive(False)
