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
from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import PeasGtk

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
        grid.connect("destroy", self.close_callback)

        self.entry_address = self.builder.get_object("entry_address")
        self.entry_address.set_text(self.settings.get_string("address"))

        self.spinbutton_port = self.builder.get_object("spinbutton_port")
        self.spinbutton_port.set_value(self.settings.get_int("port"))

        self.hscale_screenduration = self.builder.get_object("hscale_screenduration")
        self.hscale_screenduration.set_value(self.settings.get_int("screenduration"))

        self.hscale_scrollduration = self.builder.get_object("hscale_scrollduration")
        self.hscale_scrollduration.set_value(self.settings.get_int("scrollduration"))

        self.entry_scrollseparator = self.builder.get_object("entry_scrollseparator")
        self.entry_scrollseparator.set_text(self.settings.get_string("scrollseparator"))
        
        self.comboboxtext_scrolling = self.builder.get_object("comboboxtext_scrolling")
        self.comboboxtest_scrolling.connect("changed", comboboxtext_scrolling_callback)
        self.comboboxtext_scrolling.set_active(self.settings.get_enum("scrolling"))

        return grid

    def comboboxtext_scrolling_callback(self, comboboxtext):
        if (comboboxtext.get_active_text() == "Rolling"):
            self.hscale_scrollduration.set_sensitive(True)
            self.entry_scrollseparator.set_sensitive(True)
        else:
            self.hscale_scrollduration.set_sensitive(False)
            self.entry_scrollseparator.set_sensitive(False)

    def close_callback(self, widget):
        self.settings.set_string("address", self.entry_address.get_text())
        self.settings.set_int("port", self.spinbutton_port.get_value())
        self.settings.set_int("screenduration", self.hscale_screenduration.get_value())
        self.settings.set_int("scrollduration", self.hscale_scrollduration.get_value())
        self.settings.set_string("scrollseparator", self.entry_scrollseparator.get_text())
        self.settings.set_enum("scrolling", self.comboboxtext_scrolling.get_active())
