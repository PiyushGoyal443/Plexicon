'''
Created on Jun 22, 2011

@author: dibyendu
'''

import gtk
import getdata
import parser

class PyApp(gtk.Window):

    def __init__(self):
        super(PyApp, self).__init__()
        self.set_title("Entry")
        self.set_size_request(250, 28)
        self.set_decorated(False)
        self.set_position(gtk.WIN_POS_MOUSE)
        entry = gtk.Entry()
        entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        self.add(entry)
        entry.connect("key-release-event", self.on_key_release)
        self.connect("destroy", gtk.main_quit)
        self.show_all()

    def on_key_release(self, widget, event):
        if event.keyval == gtk.keysyms.Return:
            data = getdata.getData(widget.get_text())
            print data

PyApp()
gtk.main()