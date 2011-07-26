'''
@author: dibyendu das

This module contains the class; object 
of which displays all the favourite words
of the user in an alphabetic arrangement
'''

import gtk
from path import FAVOURITE_ICON_PATH

class Favourite(gtk.Window):
    '''
    object of this class is a window which
    stores user's favourite words
    '''

    def __init__(self):
        super(Favourite, self).__init__()
        self.set_title('Favourites')
        self.set_size_request(400, 400)
        self.set_modal(True)
        self.set_border_width(10)
        self.connect('delete-event', self.hide)
        self.set_icon_from_file(FAVOURITE_ICON_PATH)
        self.__link_state = False

    def hide(self, unused_window = None, unused_event = None,
             called_by_link = False):
        'hides the favourite window'

        self.hide_all()
        self.remove(self.get_child())
        gtk.main_quit()
        self.__link_state = called_by_link
        return True

    def show(self, notebook):
        'exposes the favourite window'

        if len(notebook) > 1:
            for index in range(26):
                tab = gtk.Label('%s' % chr(ord('A') + index))
                notebook[0].append_page(notebook[1][chr(ord('A') + index)],
                                        tab)
            del notebook[1]
        self.add(notebook[0])
        self.show_all()
        gtk.main()
        if self.__link_state:
            self.__link_state = False
            gtk.main_quit()
        return False