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
        str = '<span font_desc="Sans Bold 17" font_family="Serif">  %s  </span>' % (word.query)
        (attr, defaultText, char) = pango.parse_markup(str, accel_marker = u'\x00')
        label = gtk.Label()
        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 0.0, yscale = 0.0)
        hBox = gtk.HBox(spacing = 10)
        label.set_attributes(attr)
        label.set_text(defaultText)
        height = width = not themeIndex and 60 or 32
        speaker = Speaker(themeIndex, width, height)
        if word.soundUrl:
            speaker.connect("speaker_on", self.playText, '', word.soundUrl)
        else:
            speaker.connect("speaker_on", self.playText, word.query)
        hBox.pack_start(label)
        hBox.pack_start(speaker())
        alignment.add(hBox)
        vBox.pack_start(alignment)
        str = ''
        for meaning in word.meaning: str += u'<span font_desc="Sans 12" font_family="Serif">\n\t'\
+ meaning + '</span>'
        if str:
            (attr, defaultText, char) = pango.parse_markup(str, accel_marker = u'\x00')
            label = gtk.Label()
            label.set_attributes(attr)
            label.set_text(defaultText)
            alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 0.0, yscale = 0.0)
            alignment.add(label)
            vBox.pack_start(alignment)
        if word.image:
            imageFile = HomePath + '/.plexicon/image.gif'
            file = open(imageFile, 'wb')
            file.write(word.image)
            file.close()
            image = gtk.image_new_from_pixbuf(gtk.gdk.pixbuf_new_from_file(imageFile))
            fixed = gtk.Fixed()
            x = 500 >= image.requisition.width and (500 - image.requisition.width) / 2 or 0
            fixed.put(image, x, 0)
            vBox.pack_start(gtk.Label('\n'), True, True)
            vBox.pack_start(fixed)
        alignment = gtk.Alignment(xalign = 0.0, yalign = 0.0, xscale = 0.0, yscale = 0.0)
        alignment.add(vBox)
        self.scroll.add_with_viewport(alignment)
        self.scroll.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
