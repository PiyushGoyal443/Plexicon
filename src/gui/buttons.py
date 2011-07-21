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
        return True

    def button_off(self, unused_eventbox, unused_event, data):
        self.alignment.window.set_cursor(None)
        data.set_from_pixbuf(self.__off)
        return True

    def activate_button(self, unused_eventbox, unused_event):
        self.emit(self.__signal)
        return True

    def __init__(self, path_index, on_file, off_file, signal, width, height,
                 xalign, yalign):
        self.__gobject_init__()
        self.__signal = signal
        self.set_resource_directory(path_index)
        on_file = self.__resource_directory + on_file
        off_file = self.__resource_directory + off_file
        try:
            self.__on = gtk.gdk.pixbuf_new_from_file(on_file)
            self.__off = gtk.gdk.pixbuf_new_from_file(off_file)
        except Exception, exception:
            print exception.message
        image_on = Image.open(on_file)
        image_off = Image.open(off_file)
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

    def __init__(self, path_index = 0, width = 40, height = 40, xalign = 0.5,
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