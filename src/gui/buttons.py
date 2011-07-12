'''
@author: dibyendu das

This is the module responsible
for creating custom buttons
'''

import gtk, gobject
import Image

index = 0

class ImageButton(gobject.GObject):
    '''
    This is a base class. It creates a custom button object
    with 7 parameters (__onFile, __offFile, signalName, width,
    height, x-align [0(left) to 1(right)] & y-align)
    '''
    __signal = ''
    __dir = ('/resource/BlackPaintSplatter/', '/resource/BlackSquare/', '/resource/BlueandWhite/',
               '/resource/GreySquare/')
    __resourceDirectory = ' '

    def __call__(self):
        return self.alignment

    def getSignal(self):
        return self.__signal

    def setResourceDirectory(self, index):
        from path import BasePath
        self.__resourceDirectory = BasePath + self.__dir[index]

    def buttonOn(self, eventBox, buttonEvent, data):
        self.alignment.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        data.set_from_pixbuf(self.__on)
        return True

    def buttonOff(self, eventBox, buttonEvent, data):
        self.alignment.window.set_cursor(None)
        data.set_from_pixbuf(self.__off)
        return True

    def activateButton(self, eventBox, buttonEvent):
        self.emit(self.__signal)
        return True

    def __init__(self, pathIndex, onFile, offFile, signal, width, height, xalign, yalign):
        self.__gobject_init__()
        self.__signal = signal
        self.setResourceDirectory(pathIndex)
        onFile = self.__resourceDirectory + onFile
        offFile = self.__resourceDirectory + offFile
        try:
            self.__on = gtk.gdk.pixbuf_new_from_file(onFile)
            self.__off = gtk.gdk.pixbuf_new_from_file(offFile)
        except Exception, e:
            print e.message
        imageOn = Image.open(onFile)
        imageOff = Image.open(offFile)
        self.__on = self.__on.scale_simple(width, height, gtk.gdk.INTERP_HYPER)
        self.__off = self.__off.scale_simple(width * imageOff.size[0] / imageOn.size[0],
                                             height, gtk.gdk.INTERP_HYPER)
        image = gtk.Image()
        eventBox = gtk.EventBox()
        self.alignment = gtk.Alignment(xalign, yalign, 0, 0)
        image.set_from_pixbuf(self.__off)
        eventBox.add(image)
        self.alignment.add(eventBox)
        eventBox.connect("enter_notify_event", self.buttonOn, image)
        eventBox.connect("leave_notify_event", self.buttonOff, image)
        eventBox.connect("button_release_event", self.activateButton)

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

    def __init__(self, pathIndex = 0, width = 40, height = 40, xalign = 0, yalign = 0.5):
        ImageButton.__init__(self, pathIndex, self.__onFile, self.__offFile, self.__signal, width, height,
                             xalign, yalign)

class Exit(ImageButton):
    '''
    This class creates a quit button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "exit" when clicked
    '''

    __onFile = 'exit_on.png'
    __offFile = "exit_off.png"
    __signal = "exit"

    def __init__(self, pathIndex = 0, width = 40, height = 40, xalign = 1, yalign = 0):
        ImageButton.__init__(self, pathIndex, self.__onFile, self.__offFile, self.__signal, width, height,
                             xalign, yalign)

class Restart(ImageButton):
    '''
    This class creates a restart button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "restart" when clicked
    '''

    __onFile = 'restart_on.png'
    __offFile = "restart_off.png"
    __signal = "restart"

    def __init__(self, pathIndex = 0, width = 40, height = 40, xalign = 0, yalign = 0):
        ImageButton.__init__(self, pathIndex, self.__onFile, self.__offFile, self.__signal, width, height,
                             xalign, yalign)

class Info(ImageButton):
    '''
    This class creates an info button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "info" when clicked
    '''

    __onFile = 'info.png'
    __offFile = "info.png"
    __signal = "info"

    def __init__(self, pathIndex = 0, width = 40, height = 40, xalign = 0.5, yalign = 0):
        ImageButton.__init__(self, pathIndex, self.__onFile, self.__offFile, self.__signal, width, height,
                             xalign, yalign)

class Search(ImageButton):
    '''
    This class creates a search button with 4 
    parameters (width, height, x-align & y-align)
    which emits a custom signal "search" when clicked
    '''

    __onFile = 'search.png'
    __offFile = "search.png"
    __signal = "search"

    def __init__(self, pathIndex = 0, width = 40, height = 40, xalign = 1, yalign = 0.5):
        ImageButton.__init__(self, pathIndex, self.__onFile, self.__offFile, self.__signal, width, height,
                             xalign, yalign)


gobject.signal_new(Speaker().getSignal(), Speaker, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
gobject.signal_new(Exit().getSignal(), Exit, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
gobject.signal_new(Restart().getSignal(), Restart, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
gobject.signal_new(Info().getSignal(), Info, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
gobject.signal_new(Search().getSignal(), Search, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
