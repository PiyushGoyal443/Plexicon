'''
@author: dibyendu das

Module to create a spinner object
'''

import gtk, cairo
from math import pi
from path import OUTPUT_ICON_PATH

class Spinner(gtk.Window):
    'creates a spinner interface'

    def __expose(self, unused, unused_event):
        'called on expose event'

        cairo_object = self.window.cairo_create()
        cairo_object.set_operator(cairo.OPERATOR_CLEAR)
        cairo_object.rectangle(0.0, 0.0, *self.get_size())
        cairo_object.fill()
        cairo_object.set_operator(cairo.OPERATOR_OVER)
        cairo_object.set_source_rgba(0, 0, 0, 0)
        cairo_object.arc(self.get_size()[0] / 2, self.get_size()[1] / 2,
                         self.get_size()[0] / 2, 0, pi * 2)
        cairo_object.fill()


    def __init__(self):
        super(Spinner, self).__init__()
        self.set_size_request(100, 100)
        self.set_position(gtk.WIN_POS_CENTER)
        icon = gtk.gdk.pixbuf_new_from_file(OUTPUT_ICON_PATH).scale_simple(
                                              48, 48, gtk.gdk.INTERP_HYPER)
        self.set_icon(icon)
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_colormap(self.get_screen().get_rgba_colormap())
        self.connect('expose-event', self.__expose)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.set_opacity(0.5)
        spinner = gtk.Spinner()
        spinner.set_tooltip_text("searching ...")
        spinner.start()
        self.add(spinner)
        self.show_all()