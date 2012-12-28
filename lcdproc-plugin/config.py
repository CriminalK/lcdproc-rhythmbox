#!/usr/bin/python
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="LCDProc-Plugin Configuration", resizable=false, )

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        label_address = Gtk.Label("Address")
        entry_address = Gtk.Entry()

        label_port = Gtk.Label("Port")
        spinbutton_port = Gtk.SpinButton()
        spinbutton_port.set_adjustment(Gtk.Adjustment(value=0, lower=0, upper=65536, step_increment=1, page_increment=5, page_size=1))
        spinbutton_port.set_numeric(True)
#        spinbutton_port.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)

        label_scrolling = Gtk.Label("Scrolling type")
        comboboxtext_scrolling = Gtk.ComboBoxText()
        comboboxtext_scrolling.append_text("Bouncing")
        comboboxtext_scrolling.append_text("Rolling")
        comboboxtext_scrolling.set_active(0)

        label_scrollduration = Gtk.Label("Scrolling duration")
        hscale_scrollduration = Gtk.HScale.new_with_range(min=1, max=100, step=1)

        label_scrollseparator = Gtk.Label("Scrolling separator")
        entry_scrollseparator = Gtk.Entry()

        label_screenduration = Gtk.Label("Screen duration")
        hscale_screenduration = Gtk.HScale.new_with_range(min=1, max=100, step=1)

        button_close = Gtk.Button(stock=Gtk.STOCK_CLOSE)

        grid.attach(label_address, 1, 1, 1, 1)
        grid.attach_next_to(entry_address, label_address, Gtk.PositionType.RIGHT, 1 ,1)
        grid.attach_next_to(label_port, label_address, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(spinbutton_port, label_port, Gtk.PositionType.RIGHT, 1 ,1)
        grid.attach_next_to(label_scrolling, label_port,  Gtk.PositionType.BOTTOM, 1 ,1)
        grid.attach_next_to(comboboxtext_scrolling, label_scrolling, Gtk.PositionType.RIGHT, 1 ,1)
        grid.attach_next_to(label_scrollduration, label_scrolling, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(hscale_scrollduration, label_scrollduration, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(label_scrollseparator, label_scrollduration, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(entry_scrollseparator, label_scrollseparator, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(label_screenduration, label_scrollseparator, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(hscale_screenduration, label_screenduration, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(button_close, hscale_screenduration, Gtk.PositionType.BOTTOM, 1, 1)

        self.add(grid)

    def on_button_clicked(self, widget):
        print "Hello World"

win = MyWindow()
win.connect("delete_event", Gtk.main_quit)
win.show_all()

Gtk.main()
