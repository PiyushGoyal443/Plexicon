'''
@author: dibyenu das

This module is used to play an
mp3 file in a separate thread.

An explicit python module 'pygst'
is required for playing sound
'''

import pygst
pygst.require("0.10")

import gst, gtk

class PlayMp3:
    '''
    This is the class which stores
    the path to the mp3 file in its
    class attribute 'file'.
    The 'file' starts playing on calling
    the method 'play()' by a PlayMp3 object
    '''

    file = ''
    def __init__(self, filePath):
        self.__class__.file = filePath
        self.player = gst.element_factory_make("playbin2")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.onMessage)

    def onMessage(self, bus, message):
        type = message.type
        if type == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.playmode = False
        elif type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            self.playmode = False
            err, debug = message.parse_error()
            print "Error: %s" % err, debug

    def play(self):
        self.playmode = True
        self.player.set_property("uri", "file://" + self.file)
        self.player.set_state(gst.STATE_PLAYING)
        while self.playmode:
            pass
        gtk.main_quit()


def playSoundFile(fileName):
    '''
    This file can be called from an outside
    module with the 'fileName' parameter
    pointing to the path of a valid mp3 file
    '''
    import os
    fileName = os.path.abspath(fileName)
    sound = PlayMp3(fileName)
    import thread
    thread.start_new_thread(sound.play, ())
    gtk.main()
    return True
