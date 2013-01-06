# Copyright (c) 2010 Loic Andrieu <looustic at gmail.com>
# Copyright (c) 2011 Nikolai Knopp <mike_rofone at imail.de>
#
# This plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject
from gi.repository import Peas
from gi.repository import RB
from gi.repository import Gio

from lcdproc.server import Server
from lcdproc_config_dialog import LCDProcPluginConfigureDialog

#Field names for DB queries
STREAM_SONG_ARTIST = 'rb:stream-song-artist'
STREAM_SONG_TITLE  = 'rb:stream-song-title'
STREAM_SONG_ALBUM  = 'rb:stream-song-album'
NORMAL_SONG_ARTIST = 'artist'
NORMAL_SONG_TITLE  = 'title'
NORMAL_SONG_ALBUM  = 'album'

#Scrolling constants
SCROLL_BOUNCING="Bouncing"
SCROLL_ROLLING="Rolling"

class LCDProcPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'LCDProcPlugin'
    object = GObject.property(type=GObject.Object)

    def __init__ (self):
        GObject.Object.__init__ (self)
        self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.lcdproc-plugin")

    def time_callback(self, player, time):
        if not self.running and not self.connect():
            # no connection to LCDd
            print "Could not reconnect to LCDd"
            return
        
        try:
            result, playing = player.get_playing()
            if not (time >= 0 and playing):
                return
            self.time_widget.set_text(self.track + " " + (("%d:%02d" % (time/60,  time % 60)) + self.duration).rjust(self.lcd.server_info["screen_width"]-len(self.track)-1))
        except:
            # connection to LCDd is broken
            self.connectionlost("time_callback");

    def change_callback(self, player, entry):
        if not self.running and not self.connect():
            # no connection to LCDd
            print "Could not reconnect to LCDd"
            return
        
        if (entry == None):
            self.title = "No playback"
            self.album = ""
            self.artist = ""
            self.duration = ""
            self.track = ""
        else:
            if entry.get_entry_type().props.category == RB.RhythmDBEntryCategory.STREAM:
                # streaming item - set station name as album and only update artist & title
                self.album = entry.get_string(RB.RhythmDBPropType.TITLE)
                self.artist = ""
                self.title = ""
                self.track = "Webradio"
                self.duration = ""
            else:
                # regular item (local DB or LastFM)
                self.artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
                self.album = entry.get_string(RB.RhythmDBPropType.ALBUM)
                self.title = entry.get_string(RB.RhythmDBPropType.TITLE)
                tracknumber = entry.get_ulong(RB.RhythmDBPropType.TRACK_NUMBER)
                if tracknumber > 0 and tracknumber < 100:
                    # valid track number
                    self.track = "Track " + str(tracknumber)
                else:
                    # invalid track number
                    self.track = ""
                seconds = entry.get_ulong(RB.RhythmDBPropType.DURATION)
                self.duration = "/%d:%02d" % (seconds/60,  seconds % 60)
        
        self.update_widgets()
    
    def update_widgets(self):
        try:
            self.set_correct_text(self.title_widget, self.title)
            self.set_correct_text(self.album_widget, self.album)
            self.set_correct_text(self.artist_widget, self.artist)
            self.set_correct_text(self.time_widget, self.duration)
         except:
            # connection to LCDd is broken
            self.connectionlost("update_widgets");

    def set_correct_text(self, widget, text):
        if (self.lcd.server_info["screen_width"] < len(text)):
            if self.scrollmode == SCROLL_ROLLING:
                text += self.scrollseparator
        else:
            text = " " * ((self.lcd.server_info["screen_width"] - len(text)) / 2) + text
        widget.set_text(text)
        
    # copied from im-status plugin
    def playing_song_property_changed (self, sp, uri, property, old, new):
        if not self.running and not self.connect():
            # no connection to LCDd
            print "Could not reconnect to LCDd"
            return

        relevant = False
        if sp.get_playing () and property in (NORMAL_SONG_ARTIST,STREAM_SONG_ARTIST):
            self.artist = new
            relevant = True
        elif sp.get_playing () and property in (NORMAL_SONG_TITLE,STREAM_SONG_TITLE):
            if new.count(" - ") >= 1:
                # contains "Artist - Title"
                fields = new.split(" - ",1)
                self.artist = fields[0]
                self.title = fields[1]
            else:
                # only title
                self.title = new
            relevant = True
        elif sp.get_playing () and property in (NORMAL_SONG_ALBUM,STREAM_SONG_ALBUM):
            self.album = new
            relevant = True
        
        if relevant:
            self.update_widgets()

    def connectionlost(self, source):
        print "in " + source + ": Connection to LCDd lost, disconnecting plugin (will try to reconnect)"
        self.disconnect()
    
    def do_activate(self):
        self.shell = self.object
        self.running = False
        self.inited = False

        if not self.connect():
             # LCDd not running
            print "LCDd not running, plugin not initialising"
            return

        self.pec_id = self.shell.props.shell_player.connect('elapsed-changed', self.time_callback)
        self.psc_id = self.shell.props.shell_player.connect('playing-song-changed', self.change_callback)
        self.pspc_id = self.shell.props.shell_player.connect ('playing-song-property-changed', self.playing_song_property_changed)
        # The plugin is listening to changes to the settings file; when the settings are changed using the control panel, the plugin is restarted
        # As a temporary fix (to stop the plugin from restarting for each update), the plugin only listens to updates of the scrolling setting
        self.c_id = self.settings.connect("changed::scrolling", self.changed_settings_callback)

        self.change_callback(self.shell.props.shell_player,self.shell.props.shell_player.get_playing_entry())

        print "Connected to LCDProc, loading plugin"

    def changed_settings_callback(self, settings, key):
        self.disconnect()
        self.connect()

    def connect(self):
        try:
            self.lcd = Server(hostname=self.settings.get_string("address"), port=self.settings.get_int("port"))
        except:
            # LCDd not running
            self.running = False
            return False

        self.scrollseparator = self.settings.get_string("scrollseparator")
        self.scrollmode = self.settings.get_string("scrolling")
        if (self.scrollmode == SCROLL_ROLLING):
            direction = "m"
        else:
            direction = "h"

        self.lcd.start_session()
        self.running = True
        
        self.screen1 = self.lcd.add_screen("Screen1")
        self.screen1.set_heartbeat("off")
        self.screen1.set_priority("foreground")
        self.screen1.set_duration(self.settings.get_int("screenduration"))

        self.title_widget = self.screen1.add_scroller_widget("Widget1", left = 1, top = 1, right = self.lcd.server_info["screen_width"], bottom = 1, direction = direction, speed = self.settings.get_int("scrollduration"), text="")
        self.artist_widget = self.screen1.add_scroller_widget("Widget2", left = 1, top = 2, right = self.lcd.server_info["screen_width"], bottom = 2, direction = direction, speed = self.settings.get_int("scrollduration"), text="")

        if (self.lcd.server_info["screen_height"] < 4):
            self.screen2 = self.lcd.add_screen("Screen2")
            self.screen2.set_heartbeat("off")
            self.screen2.set_priority("foreground")
            self.screen2.set_duration(self.settings.get_int("screenduration"))

            self.album_widget = self.screen2.add_scroller_widget("Widget3", left = 1, top = 1, right = self.lcd.server_info["screen_width"], bottom = 1, direction = direction, speed = self.settings.get_int("scrollduration"), text="")
            self.time_widget = self.screen2.add_scroller_widget("Widget4", left = 1, top = 2, right = self.lcd.server_info["screen_width"], bottom = 2, direction = direction, speed = self.settings.get_int("scrollduration"), text="")
        else:
            self.album_widget = self.screen1.add_scroller_widget("Widget3", left = 1, top = 3, right = self.lcd.server_info["screen_width"], bottom = 3, direction = direction, speed = self.settings.get_int("scrollduration"), text="")
            self.time_widget = self.screen1.add_scroller_widget("Widget4", left = 1, top = 4, right = self.lcd.server_info["screen_width"], bottom = 4, direction = direction, speed = self.settings.get_int("scrollduration"), text="")
       
        print "(Re-)Connected to LCDProc"
        return True

    def do_deactivate(self):
        self.disconnect()

        if self.inited:
            #plugin was running at some point
            self.inited = False

            self.shell.props.shell_player.disconnect(self.psc_id)
            self.shell.props.shell_player.disconnect(self.pspc_id)
            self.shell.props.shell_player.disconnect(self.pec_id)
            self.settings.disconnect(self.c_id)
            del self.psc_id
            del self.pspc_id
            del self.pec_id
            del self.c_id

        del self.shell
        print "Plugin unloaded"

    def disconnect(self):
        if not self.running:
            # LCDd was not running, nothing to clean up
            return
        
        self.running = False;

        del self.scrollmode
        del self.title_widget
        del self.album_widget
        del self.artist_widget
        del self.time_widget
        del self.screen1
        try:
            del self.screen2
        except:
            pass
        self.lcd.tn.close()

        del self.lcd
        print "Plugin disconnected"
