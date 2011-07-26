# -*- coding: UTF-8 -*-
'''
@author: dibyendu das

This module parses the information stored in
the WordInfo class object of the lang.bengali
module & passes to the output interface via a
scroll-window widget
'''

import gtk, pango
from gui.buttons import Speaker, Star
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

        import urllib
        try:
            urllib.urlopen('http://www.google.co.in/')
        except IOError:
            from path import ERROR_PATH
            data = open(ERROR_PATH).read()
        else:
            if url:
                data = urllib.urlopen(url).read()
            else:
                import re, tts
                text = re.sub('[^a-zA-Z0-9 \t.,;\'":(){}\[\]%!?/]', '', text)
                data = ''
                while len(text) > 100:
                    data += tts.text_to_speech(text[:100])
                    text = text[100:]
                data += tts.text_to_speech(text)
        finally:
            sound_file_path = HOME_PATH + '/.plexicon/data/sound.mp3'
            sound_file = open(sound_file_path, 'wb')
            sound_file.write(data)
            sound_file.close()
            import sound
            import thread
            thread.start_new_thread(self.__block, ())
            if sound.play_sound_file(sound_file_path):
                thread.start_new_thread(self.__un_block, ())
            return False

    def __update_database(self, star, word):
        'updates database when a word is starred/unstarred'

        from database import DataBase
        import pickle
        database = DataBase()
        table = (len(word.query) > 1 and word.query[1] != ' ') and\
                                    word.query[:2] or word.query[:1]
        data = star.state == True and pickle.dumps(word) or None
        database.update(table.lower(), (word.query.lower(), data, 'bengali'))
        database.close()

    def __call__(self):
        return self.scroll

    def __init__(self, word, theme_index, star_state = False):
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_size_request(500, 400)
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        v_box = gtk.VBox()
        self.__block_list = []
        string = '<span font_desc="Sans Bold 17" font_family="Serif">%s</s\
pan>' % (word.query)
        (attr, default_text, unused_char) = pango.parse_markup(
                                 string, accel_marker = u'\x00')
        label = gtk.Label()
        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                  xscale = 0.0, yscale = 0.0)
        h_box = gtk.HBox(spacing = 10)
        label.set_attributes(attr)
        label.set_text(default_text)
        unused = gtk.Label('')
        unused.set_selectable(True)
        label.set_selectable(True)
        height = width = not theme_index and 60 or 32
        speaker = Speaker(theme_index, width, height)
        speaker.set_tooltip('<span font_desc="Sans 10">spell</span>')
        if word.sound_url:
            speaker.connect("speaker_on", self.play_text, '', word.sound_url)
        else:
            speaker.connect("speaker_on", self.play_text, word.query)
        star = Star(star_state)
        star.connect("starred", self.__update_database, word)
        h_box.pack_start(unused)
        h_box.pack_start(star())
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
            label.set_selectable(True)
            alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                      xscale = 0.0, yscale = 0.0)
            alignment.add(label)
            v_box.pack_start(alignment)
        if word.image or word.alt_image:
            fixed = gtk.Fixed()
            rms = 0.0
            if word.image and word.alt_image:
                path_1, path_2 = HOME_PATH + '/.plexicon/data/image1.gif', \
                                 HOME_PATH + '/.plexicon/data/image2.gif'
                file_1, file_2 = open(path_1, 'wb'), \
                                 open(path_2, 'wb')
                file_1.write(word.image)
                file_2.write(word.alt_image)
                file_1.close()
                file_2.close()
                import Image, math, operator
                hist1 = Image.open(path_1).histogram()
                hist2 = Image.open(path_2).histogram()
                rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a -
                                      b) ** 2, hist1, hist2)) / len(hist1))
                if not rms:
                    word.alt_image = ''
            if rms != 0.0:
                image_1, image_2 = gtk.image_new_from_pixbuf(gtk.gdk. \
                                       pixbuf_new_from_file(path_1)), \
                                   gtk.image_new_from_pixbuf(gtk.gdk. \
                                       pixbuf_new_from_file(path_2))
                fixed.put(image_1, 20, 0)
                fixed.put(image_2, 40 + image_1.requisition.width, 0)
            else:
                cur = word.image == '' and [word.alt_image] or [word.image]
                path = HOME_PATH + '/.plexicon/data/image.gif'
                image_file = open(path, 'wb')
                image_file.write(cur[0])
                image_file.close()
                image = gtk.image_new_from_pixbuf(gtk.gdk.pixbuf_new_from_file(
                                                                         path))
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