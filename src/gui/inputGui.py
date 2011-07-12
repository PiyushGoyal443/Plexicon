'''
@author: dibyendu das

The input interface module
'''

import gtk
from buttons import Search
from path import InputIconPath

class InputBox(gtk.Window):
    '''
    Object of this class holds the
    input widget interface
    '''

    query = ''
    target = ''

    def __stripSpace(self, data):
        count = 0
        while count < len(data) and data[count] == ' ': count += 1
        if count == len(data) : return ''
        data = data[count:]
        word = ''
        for i in range(len(data)):
            if data[i] != ' ':
                word += data[i]
                count = 0
            else:
                count += 1
                if count == 1:
                    word += ' '
        if word[len(word) - 1] == ' ':
            word = word[0:len(word) - 1]
        return word

    def __search(self, searchButton, entry):
        if entry.get_text() == '':
            return False
        self.__class__.query = self.__stripSpace(entry.get_text().lower())
        self.__class__.target = {'English': 'en', 'Bengali': 'bn'}[self.comboBox.get_active_text()]
        self.emit('destroy')

    def __init__(self, themeIndex, defaultText = '', defaultLanguage = 0):
        super(InputBox, self).__init__()
        self.set_size_request(280, 34)
        icon = gtk.gdk.pixbuf_new_from_file(InputIconPath).scale_simple(48, 48, gtk.gdk.INTERP_HYPER)
        self.set_icon(icon)
        self.set_decorated(False)
        self.set_position(gtk.WIN_POS_MOUSE)
        self.__text = ''
        self.__cur = 0
        entry = gtk.Entry()
        entry.set_text(defaultText)
        entry.set_size_request(180, 34)
        entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        border = gtk.Border(4, 4, 4, 4)
        entry.set_inner_border(border)
        hBox = gtk.HBox()
        self.comboBox = gtk.combo_box_new_text();
        self.comboBox.append_text('English')
        self.comboBox.append_text('Bengali')
        self.comboBox.set_active(defaultLanguage)
        hBox.pack_start(self.comboBox)
        hBox.pack_start(entry)
        searchButton = Search(themeIndex, 44, 34)
        searchButton.connect("search", self.__search, entry)
        hBox.pack_start(searchButton())
        self.add(hBox)
        entry.connect("key-release-event", self.onKeyRelease)
        entry.connect("button-release-event", self.onButtonRelease)
        self.connect("destroy", gtk.main_quit)
        self.set_focus(entry)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.show_all()

    def onButtonRelease(self, widget, event):
        self.__cur = widget.get_position()
    
    def onKeyRelease(self, widget, event):
        if event.keyval == gtk.keysyms.Escape:
            self.__class__.query = ''
            self.emit("destroy")
        elif event.keyval == gtk.keysyms.Return:
            return self.__search(None, widget)
        elif event.keyval == gtk.keysyms.BackSpace:
            self.__text = widget.get_text()
            self.__cur = widget.get_position()
            return
        elif event.keyval == gtk.keysyms.Left or event.keyval == gtk.keysyms.Right:
            self.__cur = widget.get_position()
            return
        else:
            if event.keyval < 256:
                key = chr(event.keyval)
                if key == ' ' or key.isalpha() or key == "'":
                    self.__text = self.__text[:self.__cur] + key + self.__text[self.__cur:]
                    self.__cur += 1
            widget.set_text(self.__text)
            widget.set_position(self.__cur)
