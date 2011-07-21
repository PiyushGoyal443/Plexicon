# -*- coding: UTF-8 -*-
'''
@author: dibyendu das

This module parses the information stored in
the WordInfo class object of the lang.english
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
        'spells the meaning or plays the sound_file specified by the url'

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
        for part in word.parts_of_speeches:
            string = '<span font_desc="Sans Bold 17" font_family="Serif">%s\
</span><span font_desc="Sans 12" font_family="Serif" foreground="#666666">  %s\
</span><span font_desc="Ubuntu 15" font_family="Ubuntu">' % (part.word,
                                                           part.part_of_speech)
            for text in part.phonetic:
                string += '  ' + text
            string += '</span>'
            (attr, default_text, unused_char) = pango.parse_markup(string,
                                                        accel_marker = u'\x00')
            label = gtk.Label()
            alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 0.0,
                                      yscale = 0.0)
            h_box = gtk.HBox(spacing = 10)
            label.set_attributes(attr)
            label.set_text(default_text)
            height = width = not theme_index and 60 or 32
            speaker = Speaker(theme_index, width, height)
            speaker.set_tooltip('<span font_desc="Sans 10">spell</span>')
            if part.sound_url:
                speaker_id = speaker.connect("speaker_on", self.play_text, '',
                                             part.sound_url)
            else:
                speaker_id = speaker.connect("speaker_on", self.play_text,
                                             part.word)
            self.__block_list.append((speaker, speaker_id))
            h_box.pack_start(label)
            h_box.pack_start(speaker())
            alignment.add(h_box)
            v_box.pack_start(alignment)
            string = ''
            if len(part.synonym):
                string += '\n<span font_desc="Sans Bold 10" font_family="Serif\
">Synonym : </span><span font_desc="Sans 10" foreground="#006B33" font_family=\
"Serif">'
                count = 0
                for syn in part.synonym:
                    count += 1
                    if count > 8:
                        count -= 8
                        string = string[:-2]
                        string += '\n                     '
                    string += syn + ', '
                string = string[:-2]
                string += '</span>'
            if len(part.antonym):
                string += '\n<span font_desc="Sans Bold 10" font_family="Serif\
">Antonym : </span><span font_desc="Sans 10" foreground="#ff0000" font_family=\
"Serif">'
                count = 0
                for ant in part.antonym:
                    count += 1
                    if count > 8:
                        count -= 8
                        string = string[:-2]
                        string += '\n                     '
                    string += ant + ', '
                string = string[:-2]
                string += '</span>'
            if len(part.related):
                string += '\n<span font_desc="Sans Bold 10" font_family="Serif\
">Related : </span>'
                count = 0
                for tense, default_text in part.related:
                    count += 1
                    if count > 4:
                        count -= 4
                        string = string[:-4]
                        string += '\n                        '
                    string += '<span font_desc="Sans 10" foreground="#0082FF" \
font_family="Serif"><b>' + default_text + '</b><span foreground="#666666"><i><\
sub> ' + tense + '</sub></i></span></span>    '
                string = string[:-4]
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
            if part.meaning:
                index = 0
                for key in part.meaning.keys():
                    index += 1
                    string = ''
                    meaning = key.replace("<em>", '<i><u>').replace('</em>',
                                                                    '</u></i>')
                    string += '<span font_desc="Sans 11" font_family="Serif">\
\t%d.  %s</span>\n' % (index, meaning)
                    (attr, default_text, unused_char) = pango.parse_markup(
                                                string, accel_marker = u'\x00')
                    label = gtk.Label()
                    alignment = gtk.Alignment(xalign = 0.0, yalign = 0.5,
                                              xscale = 0.0, yscale = 0.0)
                    label.set_attributes(attr)
                    label.set_text(default_text)
                    height = width = not theme_index and 28 or 18
                    speaker = Speaker(theme_index, width, height, 0, 0)
                    speaker.set_tooltip('<span font_desc="Sans 10">spell</span\
>')
                    speaker_id = speaker.connect("speaker_on", self.play_text,
                                                 default_text[5:])
                    self.__block_list.append((speaker, speaker_id))
                    h_box = gtk.HBox(spacing = 10)
                    h_box.pack_start(label)
                    h_box.pack_start(speaker())
                    alignment.add(h_box)
                    v_box.pack_start(alignment)
                    string = ''
                    for default_text in part.meaning[key]:
                        default_text = default_text.replace("<em>", '<i><u><sp\
an  foreground="#984BE2">').replace('</em>', '</span></u></i>')
                        if default_text:
                            string += u'<span font_desc="Sans 10" foreground="\
#FF6A00"font_family="Serif">\t\t\u00BB ' + default_text + '</span>\n'
                    if string:
                        (attr, default_text, unused_char) = pango.parse_markup(
                                                string, accel_marker = u'\x00')
                        label = gtk.Label()
                        label.set_attributes(attr)
                        label.set_text(default_text)
                        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                                  xscale = 0.0, yscale = 0.0)
                        alignment.add(label)
                        v_box.pack_start(alignment)
            if part.example:
                string = '<span font_desc="Sans 10" foreground="#FF6A00">'
                for example in part.example:
                    example = example.replace(part.word.lower(), '<i><u><span \
foreground="#984BE2">' + part.word.lower() + '</span></u></i>')
                    string += u'\n\t\t<span foreground="#0000ff">\u2666</span>\
    ' + example
                string += '</span>\n\n'
                (attr, default_text, unused_char) = pango.parse_markup(string,
                                                        accel_marker = u'\x00')
                label = gtk.Label()
                label.set_attributes(attr)
                label.set_text(default_text)
                alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                          xscale = 0.0, yscale = 0.0)
                alignment.add(label)
                expander = gtk.Expander()
                expander.set_use_markup(True)
                expander.set_use_underline(True)
                expander.set_tooltip_markup('<span font_desc="Sans 10"><sub>cl\
ick to expand</sub></span>')
                expander.set_label('<span font_desc="Sans 10" foreground="#FF0\
000">_More Examples</span>')
                expander.set_spacing(0)
                expander.add(alignment)
                v_box.pack_start(expander)
        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0,
                                  xscale = 1.0, yscale = 0.0)
        alignment.add(v_box)
        self.scroll.add_with_viewport(alignment)
        self.scroll.get_child().modify_bg(gtk.STATE_NORMAL,
                                          gtk.gdk.color_parse('#ffffff'))