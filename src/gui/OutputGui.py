'''
@author: dibyenu das

The output interface module
'''

import gtk, buttons
from path import LICENSE_PATH, ABOUT_LOGO_PATH, OUTPUT_LOGO_PATH
from path import OUTPUT_ICON_PATH


class ExitState:
    'used as enum type to return exit status'

    EXIT = 1
    RESTART = 2

class SuggestionSearch:
    '''
    used as enum type to return status
    on whether the user has clicked any 
    link to search suggested word
    '''

    ENABLE = 1
    DISABLE = 2

class OutputBox(gtk.Window):
    '''
    Object of this class holds the
    output widget interface
    '''

    returnState = ExitState.RESTART
    link = SuggestionSearch.DISABLE
    linkText = ''

    def __quit(self, unused):
        'called on clicking exit button'

        self.__class__.returnState = ExitState.EXIT
        gtk.main_quit()

    def __restart(self, unused):
        'called on clicking re search button'

        self.__class__.returnState = ExitState.RESTART
        gtk.main_quit()

    def __about(self, unused):
        'called on clicking the about button'

        self.__about_dialogue = gtk.AboutDialog()
        self.__about_dialogue.set_name('Plexicon')
        self.__about_dialogue.set_version('1.0')
        self.__about_dialogue.set_copyright('(c) 2011-2012 Dibyendu Das')
        self.__about_dialogue.set_comments('Look up words in online dictionari\
es')
        self.__about_dialogue.set_website("https://sourceforge.net/projects/pl\
exicon")
        self.__about_dialogue.set_website_label('Get Plexicon')
        self.__about_dialogue.set_license(open(LICENSE_PATH).read())
        self.__about_dialogue.set_authors(['Dibyendu Das <dibyendu.das.in@gmai\
l.com>', ])
        logo = gtk.gdk.pixbuf_new_from_file(ABOUT_LOGO_PATH).scale_simple(60,
                                                     60, gtk.gdk.INTERP_HYPER)
        self.__about_dialogue.set_logo(logo)
        self.__about_dialogue.set_icon(logo)
        self.__about_dialogue.run()
        self.__about_dialogue.destroy()

    def __init__(self, widget, theme_index):
        super(OutputBox, self).__init__()
        button_box = gtk.HBox()
        button_box.set_size_request(500, 40)
        fixed = gtk.Fixed()
        exit_button = buttons.Exit(theme_index, 40, 40)
        exit_button.connect("exit", self.__quit)
        exit_button.set_tooltip('<b><span font_desc="Sans 10" foreground="#ff0\
000">Exit</span></b>')
        button_box.pack_end(exit_button())
        restart_button = buttons.Restart(theme_index, 40, 40)
        restart_button.connect("restart", self.__restart)
        restart_button.set_tooltip('<b><span font_desc="Sans 10" foreground="#\
0000ff">Re Search</span></b>')
        button_box.pack_start(restart_button())
        logo = gtk.gdk.pixbuf_new_from_file(OUTPUT_LOGO_PATH)
        logo = logo.scale_simple(500, 60, gtk.gdk.INTERP_HYPER)
        info_button = buttons.Info(theme_index, 40, 40)
        info_button.connect("info", self.__about)
        info_button.set_tooltip('<span font_desc="Sans 10"><sub>  about\n</sub\
><i><b><span font_desc="Sans 10" foreground="#0000ff"><sup>plexicon</sup></spa\
n></b></i></span>')
        button_box.pack_start(info_button())
        fixed.put(button_box, 0, 0)
        fixed.put(widget, 0, 44)
        image = gtk.Image()
        image.set_from_pixbuf(logo)
        fixed.put(image, 0 , 448)
        self.add(fixed)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#70EDF7'))
        self.set_icon_from_file(OUTPUT_ICON_PATH)
        self.show_all()
