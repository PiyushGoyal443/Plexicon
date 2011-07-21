'''
@author: dibyendu das

The input interface module
'''

import gtk
from buttons import Search
from path import INPUT_ICON_PATH

def strip_space(data):
    'strips out any white space from a string'

    count = 0
    while count < len(data) and data[count] == ' ':
        count += 1
    if count == len(data) :
        return ''
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

class InputBox(gtk.Window):
    '''
    Object of this class holds the
    input widget interface
    '''

    query = ''
    target = ''

    def __search(self, unused_search_button, entry):
        'returns word to search for from the input widget'

        if entry.get_text() == '':
            return False
        self.__class__.query = strip_space(entry.get_text().lower())
        self.__class__.target = {'English': 'en', 'Bengali': 'bn'}\
                                [self.combo_box.get_active_text()]
        self.emit('destroy')

    def __init__(self, theme_index, default_text = '', default_language = 0,
                 editable = True):
        super(InputBox, self).__init__()
        self.set_size_request(280, 34)
        icon = gtk.gdk.pixbuf_new_from_file(INPUT_ICON_PATH).scale_simple(48,
                                            48, gtk.gdk.INTERP_HYPER)
        self.set_icon(icon)
        self.set_decorated(False)
        self.set_position(gtk.WIN_POS_MOUSE)
        self.__text = default_text
        self.__cur = len(default_text)
        entry = gtk.Entry()
        entry.set_editable(editable)
        entry.set_text(default_text)
        entry.set_size_request(180, 34)
        entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
        border = gtk.Border(4, 4, 4, 4)
        entry.set_inner_border(border)
        entry.set_tooltip_markup('<sub>press <i><b>ENTER</b></i> to search\npr\
ess <i><b>ESC</b></i> to exit</sub>')
        h_box = gtk.HBox()
        self.combo_box = gtk.combo_box_new_text()
        self.combo_box.append_text('English')
        self.combo_box.append_text('Bengali')
        self.combo_box.set_active(default_language)
        h_box.pack_start(self.combo_box)
        h_box.pack_start(entry)
        search_button = Search(theme_index, 44, 34)
        search_button.connect("search", self.__search, entry)
        search_button.set_tooltip('click to search')
        h_box.pack_start(search_button())
        self.add(h_box)
        entry.connect("key-release-event", self.on_key_release, editable)
        entry.connect("button-release-event", self.on_button_release)
        self.connect("destroy", gtk.main_quit)
        self.set_focus(entry)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.show_all()

    def on_button_release(self, widget, unused_event):
        'called on mouse button-release event'

        self.__cur = widget.get_position()

    def on_key_release(self, widget, event, editable):
        'called on key-release event'

        if event.keyval == gtk.keysyms.Escape:
            self.__class__.query = ''
            self.emit("destroy")
        elif event.keyval == gtk.keysyms.Return:
            return self.__search(None, widget)
        elif event.keyval == gtk.keysyms.BackSpace:
            self.__text = widget.get_text()
            self.__cur = widget.get_position()
            return
        elif event.keyval == gtk.keysyms.Left or event.keyval == \
                                                 gtk.keysyms.Right:
            self.__cur = widget.get_position()
            return
        else:
            if editable:
                if event.keyval < 256:
                    key = chr(event.keyval)
                    if key == ' ' or key.isalpha() or key == "'":
                        self.__text = self.__text[:self.__cur] + key + \
                                      self.__text[self.__cur:]
                        self.__cur += 1
                widget.set_text(self.__text)
                widget.set_position(self.__cur)