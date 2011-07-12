'''
@author: dibyendu das

Module to create a spinner object
'''

import gtk
from path import InputIconPath

class Spinner(gtk.Window):
    def __init__(self):
        super(Spinner, self).__init__()
        self.set_size_request(80, 80)
        self.set_position(gtk.WIN_POS_CENTER)
        icon = gtk.gdk.pixbuf_new_from_file(InputIconPath).scale_simple(48, 48, gtk.gdk.INTERP_HYPER)
        self.set_icon(icon)
        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        spinner = gtk.Spinner()
        spinner.start()
        self.add(spinner)
        self.show_all()
