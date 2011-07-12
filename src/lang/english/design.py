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
from path import HomePath

class LayOut:
    '''
    Object of this class holds the widget
    containing the formatted definition
    '''

    def __block(self):
        for tuple in self.__blockList:
            tuple[0].handler_block(tuple[1])

    def __unBlock(self):
        for tuple in self.__blockList:
            tuple[0].handler_unblock(tuple[1])

    def playText(self, speaker, text, url = ''):
        if url:
            import urllib
            data = urllib.urlopen(url).read()
        else:
            import re
            text = re.sub('[^a-zA-Z0-9 \t.,;\'":(){}\[\]%!?/]', '', text)
            import tts
            data = ''
            while len(text) > 100:
                data += tts.textToSpeech(text[:100])
                text = text[100:]
            data += tts.textToSpeech(text)
        soundFile = HomePath + '/.plexicon/sound.mp3'
        file = open(soundFile, 'wb')
        file.write(data)
        file.close()
        import sound
        import thread
        thread.start_new_thread(self.__block, ())
        if sound.playSoundFile(soundFile):
            for tuple in self.__blockList:
                tuple[0].handler_unblock(tuple[1])
        return True

    def __call__(self):
        return self.scroll

    def __init__(self, word, themeIndex):
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_size_request(500, 400)
        self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vBox = gtk.VBox()
        self.__blockList = []
        for part in word.partsOfSpeeches:
            str = '<span font_desc="Sans Bold 17" font_family="Serif">%s\
</span><span font_desc="Sans 12" font_family="Serif" foreground="#666666">  %s\
</span><span font_desc="Ubuntu 15" font_family="Ubuntu">' % (part.word, part.partOfSpeech)
            for text in part.phonetic:
                str += '  ' + text
            str += '</span>'
            (attr, defaultText, char) = pango.parse_markup(str, accel_marker = u'\x00')
            label = gtk.Label()
            alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 0.0, yscale = 0.0)
            hBox = gtk.HBox(spacing = 10)
            label.set_attributes(attr)
            label.set_text(defaultText)
            height = width = not themeIndex and 60 or 32
            speaker = Speaker(themeIndex, width, height)
            if part.soundUrl:
                id = speaker.connect("speaker_on", self.playText, '', part.soundUrl)
            else:
                id = speaker.connect("speaker_on", self.playText, part.word)
            self.__blockList.append((speaker, id))
            hBox.pack_start(label)
            hBox.pack_start(speaker())
            alignment.add(hBox)
            vBox.pack_start(alignment)
            str = ''
            if len(part.synonym):
                str += '\n<span font_desc="Sans Bold 10" font_family="Serif">Synonym : </span>\
<span font_desc="Sans 10" foreground="#006B33" font_family="Serif">'
                count = 0
                for syn in part.synonym:
                    count += 1
                    if count > 8:
                        count -= 8
                        str = str[:-2]
                        str += '\n                     '
                    str += syn + ', '
                str = str[:-2]
                str += '</span>'
            if len(part.antonym):
                str += '\n<span font_desc="Sans Bold 10" font_family="Serif">Antonym : </span>\
<span font_desc="Sans 10" foreground="#ff0000" font_family="Serif">'
                count = 0
                for ant in part.antonym:
                    count += 1
                    if count > 8:
                        count -= 8
                        str = str[:-2]
                        str += '\n                     '
                    str += ant + ', '
                str = str[:-2]
                str += '</span>'
            if len(part.related):
                str += '\n<span font_desc="Sans Bold 10" font_family="Serif">Related : </span>'
                count = 0
                for tense, defaultText in part.related:
                    count += 1
                    if count > 4:
                        count -= 4
                        str = str[:-4]
                        str += '\n                        '
                    str += '<span font_desc="Sans 10" foreground="#0082FF" font_family="Serif"><b>' + \
                    defaultText + '</b><span foreground="#666666"><i><sub> ' + tense + '</sub></i></span></span>    '
                str = str[:-4]
            if str:
                (attr, defaultText, char) = pango.parse_markup(str, accel_marker = u'\x00')
                label = gtk.Label()
                label.set_attributes(attr)
                label.set_text(defaultText)
                alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 0.0, yscale = 0.0)
                alignment.add(label)
                vBox.pack_start(alignment)
            if part.meaning:
                index = 0
                for key in part.meaning.keys():
                    index += 1
                    str = ''
                    meaning = key.replace("<em>", '<i><u>').replace('</em>', '</u></i>')
                    str += '<span font_desc="Sans 11" font_family="Serif">\t%d.  %s</span>\n' % (index, meaning)
                    (attr, defaultText, char) = pango.parse_markup(str, accel_marker = u'\x00')
                    label = gtk.Label()
                    alignment = gtk.Alignment(xalign = 0.0, yalign = 0.5, xscale = 0.0, yscale = 0.0)
                    label.set_attributes(attr)
                    label.set_text(defaultText)
                    height = width = not themeIndex and 28 or 18
                    speaker = Speaker(themeIndex, width, height, 0, 0)
                    id = speaker.connect("speaker_on", self.playText, defaultText[5:])
                    self.__blockList.append((speaker, id))
                    hBox = gtk.HBox(spacing = 10)
                    hBox.pack_start(label)
                    hBox.pack_start(speaker())
                    alignment.add(hBox)
                    vBox.pack_start(alignment)
                    str = ''
                    for defaultText in part.meaning[key]:
                        defaultText = defaultText.replace("<em>", '<i><u><span  foreground="#984BE2">').replace('</em>', '</span></u></i>')
                        if defaultText:
                            str += u'<span font_desc="Sans 10" foreground="#FF6A00"font_family="\
Serif">\t\t\u00BB ' + defaultText + '</span>\n'
                    if str:
                        (attr, defaultText, char) = pango.parse_markup(str, accel_marker = u'\x00')
                        label = gtk.Label()
                        label.set_attributes(attr)
                        label.set_text(defaultText)
                        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 0.0, yscale = 0.0)
                        alignment.add(label)
                        vBox.pack_start(alignment)
        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 1.0, yscale = 0.0)
        alignment.add(vBox)
        self.scroll.add_with_viewport(alignment)
        self.scroll.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
