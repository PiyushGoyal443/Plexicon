'''
@author: dibyenu das

The output interface module
'''

import gtk
from path import LicensePath, AboutLogoPath, OutputLogoPath, OutputIconPath
import buttons

class ExitState:
    EXIT = 1
    RESTART = 2

class SuggestionSearch:
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
        self.__class__.returnState = ExitState.EXIT
        gtk.main_quit()

    def __restart(self, unused):
        self.__class__.returnState = ExitState.RESTART
        gtk.main_quit()

    def __about(self, unused):
        self.__aboutDialogue = gtk.AboutDialog()
        self.__aboutDialogue.set_name('Plexicon')
        self.__aboutDialogue.set_version('0.1')
        self.__aboutDialogue.set_copyright('(c) 2011-2012 Dibyendu Das')
        self.__aboutDialogue.set_comments('Look up words in online dictionaries')
        self.__aboutDialogue.set_website("https://sourceforge.net/projects/plexicon")
        self.__aboutDialogue.set_website_label('Get Plexicon')
        self.__aboutDialogue.set_license(open(LicensePath).read())
        self.__aboutDialogue.set_authors(['Dibyendu Das <dibyendu.das.in@gmail.com>', ])
        logo = gtk.gdk.pixbuf_new_from_file(AboutLogoPath).scale_simple(60, 60, gtk.gdk.INTERP_HYPER)
        self.__aboutDialogue.set_logo(logo)
        self.__aboutDialogue.set_icon(logo)
        self.__aboutDialogue.run()
        self.__aboutDialogue.destroy()

    def __init__(self, widget, themeIndex):
        super(OutputBox, self).__init__()
        buttonBox = gtk.HBox()
        buttonBox.set_size_request(500, 40)
        fixed = gtk.Fixed()
        exitButton = buttons.Exit(themeIndex, 40, 40)
        exitButton.connect("exit", self.__quit)
        buttonBox.pack_end(exitButton())
        restartButton = buttons.Restart(themeIndex, 40, 40)
        restartButton.connect("restart", self.__restart)
        buttonBox.pack_start(restartButton())
        logo = gtk.gdk.pixbuf_new_from_file(OutputLogoPath)
        logo = logo.scale_simple(500, 60, gtk.gdk.INTERP_HYPER)
        infoButton = buttons.Info(themeIndex, 40, 40)
        infoButton.connect("info", self.__about)
        buttonBox.pack_start(infoButton())
        fixed.put(buttonBox, 0, 0)
        fixed.put(widget, 0, 44)
        image = gtk.Image()
        image.set_from_pixbuf(logo)
        fixed.put(image, 0 , 448)
        self.add(fixed)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#70EDF7'))
        self.set_icon_from_file(OutputIconPath)
        self.show_all()
