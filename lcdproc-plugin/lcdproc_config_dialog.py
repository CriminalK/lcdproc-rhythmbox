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
    BASE_KEY = "org.gnome.rhythmbox.plugins.lcdproc-plugin"

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings.new(self.BASE_KEY)

    def do_create_configure_widget(self):
        builder_file = rb.find_plugin_file(self, "config_dlg.glade")
        builder = Gtk.Builder()
        builder.add_from_file(builder_file)

        dialog = builder.get_object('config_dialog')
        scrolling_combobox = builder.get_object("scrolling_combobox")

        scrolling_combobox.set_active(self.settings.get_enum("scrolling"))

        dialog.connect("response", self.dialog_response)
        scrolling_combobox.connect("changed", self.scrolling_combobox_changed)

        dialog.present()
        return dialog

    def dialog_response (self, dialog, response):
        dialog.hide()

    def scrolling_combobox_changed (self, combobox):
        scrolling = combobox.get_active()
        self.settings.set_enum("scrolling", scrolling)
        #__init__.LCDProcPlugin.scrolling.set_scrollmode(scrolling)
