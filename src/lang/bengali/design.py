# -*- coding: UTF-8 -*-
'''
@author: dibyendu das

This module parses the information stored in
the WordInfo class object of the lang.bengali
module & passes to the output interface via a
scroll-window widget
'''

import gtk, pango
from gui.buttons import Speaker
from path import HOME_PATH

class LayOut:
    '''
    Object of this class holds the widget
    containing the formatted definition
    '''

    def __block(self):
        'blocks all the other speaker objects'

        for speaker_tuple in self.__block_list:
            speaker_tuple[0].handler_block(speaker_tuple[1])

    def __un_block(self):
        'unblocks all the other speaker objects'

        for speaker_tuple in self.__block_list:
            speaker_tuple[0].handler_unblock(speaker_tuple[1])

    def play_text(self, unused_speaker, text, url = ''):
        'spells the meaning or plays the sound_file_path specified by the url'

        if url:
            import urllib
            data = urllib.urlopen(url).read()
        else:
            import re
            text = re.sub('[^a-zA-Z0-9 \t.,;\'":(){}\[\]%!?/]', '', text)
            import tts
            data = ''
            while len(text) > 100:
                data += tts.text_to_speech(text[:100])
                text = text[100:]
            data += tts.text_to_speech(text)
        sound_file_path = HOME_PATH + '/.plexicon/sound.mp3'
        sound_file = open(sound_file_path, 'wb')
        sound_file.write(data)
        sound_file.close()
        import sound
        import thread
        thread.start_new_thread(self.__block, ())
        if sound.play_sound_file(sound_file_path):
            thread.start_new_thread(self.__un_block, ())
        return True

    def __call__(self):
        return self.scroll

    def __init__(self, word, theme_index):
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_size_request(500, 400)
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        v_box = gtk.VBox()
        self.__block_list = []
        string = '<span font_desc="Sans Bold 17" font_family="Serif">  %s  </s\
pan>' % (word.query)
        (attr, default_text, unused_char) = pango.parse_markup(
                                 string, accel_marker = u'\x00')
        label = gtk.Label()
        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                  xscale = 0.0, yscale = 0.0)
        h_box = gtk.HBox(spacing = 10)
        label.set_attributes(attr)
        label.set_text(default_text)
        height = width = not theme_index and 60 or 32
        speaker = Speaker(theme_index, width, height)
        speaker.set_tooltip('<span font_desc="Sans 10">spell</span>')
        if word.sound_url:
            speaker.connect("speaker_on", self.play_text, '', word.sound_url)
        else:
            speaker.connect("speaker_on", self.play_text, word.query)
        h_box.pack_start(label)
        h_box.pack_start(speaker())
        alignment.add(h_box)
        v_box.pack_start(alignment)
        string = ''
        for meaning in word.meaning:
            string += u'<span font_desc="Sans 12" font_family="Serif">\n\t'\
            + meaning + '</span>'
        if string:
            (attr, default_text, unused_char) = pango.parse_markup(string,
                                                    accel_marker = u'\x00')
            label = gtk.Label()
            label.set_attributes(attr)
            label.set_text(default_text)
            alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                      xscale = 0.0, yscale = 0.0)
            alignment.add(label)
            v_box.pack_start(alignment)
        if word.image:
            image_file_path = HOME_PATH + '/.plexicon/image.gif'
            image_file = open(image_file_path, 'wb')
            image_file.write(word.image)
            image_file.close()
            image = gtk.image_new_from_pixbuf(gtk.gdk.pixbuf_new_from_file(
                                                            image_file_path))
            fixed = gtk.Fixed()
            x_coordinate = 500 >= image.requisition.width and (500 - \
                                              image.requisition.width) / 2 or 0
            fixed.put(image, x_coordinate, 0)
            v_box.pack_start(gtk.Label('\n'), True, True)
            expander = gtk.Expander()
            expander.set_use_markup(True)
            expander.set_use_underline(True)
            expander.set_tooltip_markup('<span font_desc="Sans 10"><sub>click \
to expand</sub></span>')
            expander.set_label('<span font_desc="Sans 10" foreground="#ff0000"\
>===============   <span foreground="#0000ff">_More Definitions</span>   =====\
===========</span>')
            expander.set_spacing(10)
            expander.add(fixed)
            v_box.pack_start(expander)
        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                  xscale = 0.0, yscale = 0.0)
        alignment.add(v_box)
        self.scroll.add_with_viewport(alignment)
        self.scroll.get_child().modify_bg(gtk.STATE_NORMAL,
                                          gtk.gdk.color_parse('#ffffff'))