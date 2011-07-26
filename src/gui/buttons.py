'''
@author: dibyendu das

This is the module responsible
for creating custom buttons
'''

import gtk, gobject
import Image

class ImageButton(gobject.GObject):
    '''
    This is a base class. It creates a custom button object
    with 7 parameters (__onFile, __offFile, signalName, width,
    height, x-align [0(left) to 1(right)] & y-align)
    '''

    __signal = ''
    __dir = ('/resource/BlackPaintSplatter/', '/resource/BlackSquare/',
             '/resource/BlueandWhite/', '/resource/GreySquare/')
    __resource_directory = ' '

    def __call__(self):
        return self.alignment

    def get_signal(self):
        return self.__signal

    def set_tooltip(self, text):
        self.image.set_tooltip_markup(text)

    def set_resource_directory(self, index):
        from path import BASE_PATH
        self.__resource_directory = BASE_PATH + self.__dir[index]

    def button_on(self, unused_eventbox, unused_event, data):
        self.alignment.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        data.set_from_pixbuf(self.__on)
        return False

    def button_off(self, unused_eventbox, unused_event, data):
        self.alignment.window.set_cursor(None)
        data.set_from_pixbuf(self.__off)
        return False

    def activate_button(self, unused_eventbox, unused_event):
        self.emit(self.__signal)
        return False

    def __init__(self, path_index, on_file, off_file, signal, width, height,
                 xalign, yalign):
        self.__gobject_init__()
        self.__signal = signal
        self.set_resource_directory(path_index)
        self.__on = gtk.gdk.pixbuf_new_from_file(self.__resource_directory +
                                                 on_file)
        self.__off = gtk.gdk.pixbuf_new_from_file(self.__resource_directory +
                                                  off_file)
        image_on = Image.open(self.__resource_directory + on_file)
        image_off = Image.open(self.__resource_directory + off_file)
        self.__on = self.__on.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
        self.__off = self.__off.scale_simple(
    width * image_off.size[0] / image_on.size[0], height, gtk.gdk.INTERP_HYPER)
        self.image = gtk.Image()
        event_box = gtk.EventBox()
        self.alignment = gtk.Alignment(xalign, yalign, 0, 0)
        self.image.set_from_pixbuf(self.__off)
        event_box.add(self.image)
        self.alignment.add(event_box)
        event_box.connect("enter_notify_event", self.button_on, self.image)
        event_box.connect("leave_notify_event", self.button_off, self.image)
        event_box.connect("button_release_event", self.activate_button)

gobject.type_register(ImageButton)

class Speaker(ImageButton):
    '''
    This class creates a speaker button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "speaker_on" when clicked
    '''

    __onFile = 'speaker_on.png'
    __offFile = 'speaker_off.png'
    __signal = "speaker_on"

    def __init__(self, path_index = 0, width = 40, height = 40, xalign = 0,
                 yalign = 0.5):
        ImageButton.__init__(self, path_index, self.__onFile, self.__offFile,
                             self.__signal, width, height, xalign, yalign)

class Exit(ImageButton):
    '''
    This class creates a quit button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "exit" when clicked
    '''

    __onFile = 'exit_on.png'
    __offFile = "exit_off.png"
    __signal = "exit"

    def __init__(self, path_index = 0, width = 40, height = 40, xalign = 1,
                 yalign = 0):
        ImageButton.__init__(self, path_index, self.__onFile, self.__offFile,
                             self.__signal, width, height, xalign, yalign)

class Restart(ImageButton):
    '''
    This class creates a restart button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "restart" when clicked
    '''

    __onFile = 'restart_on.png'
    __offFile = "restart_off.png"
    __signal = "restart"

    def __init__(self, path_index = 0, width = 40, height = 40, xalign = 0,
                 yalign = 0):
        ImageButton.__init__(self, path_index, self.__onFile, self.__offFile,
                             self.__signal, width, height, xalign, yalign)

class Info(ImageButton):
    '''
    This class creates an info button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "info" when clicked
    '''

    __onFile = 'info.png'
    __offFile = "info.png"
    __signal = "info"

    def __init__(self, path_index = 0, width = 40, height = 40, xalign = 0.72,
                 yalign = 0):
        ImageButton.__init__(self, path_index, self.__onFile, self.__offFile,
                             self.__signal, width, height, xalign, yalign)

class Search(ImageButton):
    '''
    This class creates a search button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "search" when clicked
    '''

    __onFile = 'search.png'
    __offFile = "search.png"
    __signal = "search"

    def __init__(self, path_index = 0, width = 40, height = 40, xalign = 1,
                 yalign = 0.5):
        ImageButton.__init__(self, path_index, self.__onFile, self.__offFile,
                             self.__signal, width, height, xalign, yalign)

class Query(ImageButton):
    '''
    This class creates a query button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "query" when clicked
    '''

    __onFile = 'database_on.png'
    __offFile = "database_off.png"
    __signal = "query"

    def __init__(self, path_index = 0, width = 40, height = 40, xalign = 0.28,
                 yalign = 0):
        ImageButton.__init__(self, path_index, self.__onFile, self.__offFile,
                             self.__signal, width, height, xalign, yalign)

class Star(gobject.GObject):
    '''
    This class creates a star(favourite) button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "starred" when clicked
    '''

    def __call__(self):
        return self.alignment

    def set_tooltip(self, text):
        self.image.set_tooltip_markup(text)

    def button_on(self, unused_eventbox, unused_event):
        self.alignment.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        return False

    def button_off(self, unused_eventbox, unused_event):
        self.alignment.window.set_cursor(None)
        return False

    def __toggle_button(self, unused_eventbox, unused_event):
        if self.state:
            self.state = False
        else: self.state = True
        pixbuf = self.state and self.__on or self.__off
        self.image.set_from_pixbuf(pixbuf)
        self.emit('starred')
        return False

    def __init__(self, state, width = 20, height = 20, xalign = 1.0,
                 yalign = 0.5):
        self.__gobject_init__()
        from path import BASE_PATH
        self.__on = gtk.gdk.pixbuf_new_from_file(BASE_PATH + '/resource/starred.gif')
        self.__off = gtk.gdk.pixbuf_new_from_file(BASE_PATH + '/resource/unstarred.gif')
        self.__on = self.__on.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
        self.__off = self.__off.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
        self.image = gtk.Image()
        event_box = gtk.EventBox()
        self.alignment = gtk.Alignment(xalign, yalign, 0, 0)
        self.state = state
        current_pixbuf = state and self.__on or self.__off
        self.image.set_from_pixbuf(current_pixbuf)
        event_box.add(self.image)
        self.alignment.add(event_box)
        event_box.connect("enter_notify_event", self.button_on)
        event_box.connect("leave_notify_event", self.button_off)
        event_box.connect("button_release_event", self.__toggle_button)

gobject.type_register(Star)

gobject.signal_new(Speaker().get_signal(), Speaker, gobject.SIGNAL_RUN_LAST,
                   gobject.TYPE_NONE, ())
gobject.signal_new(Exit().get_signal(), Exit, gobject.SIGNAL_RUN_LAST,
                   gobject.TYPE_NONE, ())
gobject.signal_new(Restart().get_signal(), Restart, gobject.SIGNAL_RUN_LAST,
                   gobject.TYPE_NONE, ())
gobject.signal_new(Info().get_signal(), Info, gobject.SIGNAL_RUN_LAST,
                   gobject.TYPE_NONE, ())
gobject.signal_new(Search().get_signal(), Search, gobject.SIGNAL_RUN_LAST,
                   gobject.TYPE_NONE, ())
gobject.signal_new(Query().get_signal(), Query, gobject.SIGNAL_RUN_LAST,
                   gobject.TYPE_NONE, ())
gobject.signal_new('starred', Star, gobject.SIGNAL_RUN_LAST,
                   gobject.TYPE_NONE, ())