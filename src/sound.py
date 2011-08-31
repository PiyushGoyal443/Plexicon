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
    def __init__(self, file_path):
        self.__class__.file = file_path
        self.player = gst.element_factory_make("playbin2")
        self.__playmode = True
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.__on_message)

    def __on_message(self, unused_bus, message):
        '''
        called if some events happen
        during play
        '''

        message_type = message.type
        if message_type == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.__playmode = False
        elif message_type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            self.__playmode = False
            err, debug = message.parse_error()
            print "Error: %s" % err, debug

    def play(self):
        'plays the file'

        self.__playmode = True
        self.player.set_property("uri", "file://" + self.file)
        self.player.set_state(gst.STATE_PLAYING)
        while self.__playmode:
            pass
        return True


def play_sound_file(file_name):
    '''
    This file can be called from an outside
    module with the 'file_name' parameter
    pointing to the path of a valid mp3 file
    '''

    import os
    file_name = os.path.abspath(file_name)
    sound = PlayMp3(file_name)
    sound.play()
    return True