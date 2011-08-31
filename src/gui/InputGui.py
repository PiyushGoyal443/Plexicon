'''
@author: dibyendu das

The input interface module
'''

import gtk
from buttons import Search
from path import INPUT_ICON_PATH

class InputBox(gtk.Window):
    '''
    Object of this class holds the
    input widget interface
    '''

    query = ''
    target = ''
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' "

    def __search(self, unused_search_button, entry):
        'returns word to search for from the input widget'

        if entry.get_text() == '':
            return False
        self.__class__.query = entry.get_text().lower()
        self.__class__.target = {'English': 'en', 'Bengali': 'bn'}\
                                [self.combo_box.get_active_text()]
        self.emit('destroy')

    def __init__(self, theme_index, default_text = '', default_language = 0):
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
        entry.connect("key-release-event", self.__on_key_release)
        entry.connect("button-release-event", self.__on_button_release)
        entry.connect_after("paste-clipboard", self.__on_paste_text)
        self.connect("destroy", gtk.main_quit)
        self.set_focus(entry)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
        self.show_all()

    def __on_paste_text(self, entry):
        'called on pasting text '

        self.__text = entry.get_text()
        self.__cur = entry.get_position()
        return False

    def __on_button_release(self, widget, unused_event):
        'called on mouse button-release event'

        self.__cur = widget.get_position()

    def __on_key_release(self, widget, event):
        'called on key-release event'

        if event.keyval == gtk.keysyms.Escape:
            self.__class__.query = ''
            self.emit("destroy")
        elif event.keyval == gtk.keysyms.Return:
            return self.__search(None, widget)
        if event.keyval < 256 and chr(event.keyval) in self.__class__.valid_chars:
            if len(widget.get_text()) <= len(self.__text):
                self.__text = widget.get_text()
                self.__cur = widget.get_position()
            else:
                self.__text = self.__text[:self.__cur] + chr(event.keyval) + \
                              self.__text[self.__cur:]
                self.__cur += 1
            widget.set_text(self.__text)
            widget.set_position(self.__cur)
        elif event.keyval in [gtk.keysyms.Left, gtk.keysyms.Right]:
            self.__text = widget.get_text()
            self.__cur = widget.get_position()
            widget.set_text(self.__text)
            widget.set_position(self.__cur)
        elif event.keyval == gtk.keysyms.BackSpace:
            self.__text = widget.get_text()
            self.__cur = widget.get_position()
        else:
            widget.set_text(self.__text)
            widget.set_position(self.__cur)
        return False