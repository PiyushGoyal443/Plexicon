'''
@author: dibyendu das

This module creates widgets containing error messages
on network timeout[via timeOut() function] or on not
finding any vaild definition [via noDefinition() function]
'''

import gtk, pango

def timeOut():
    scroll = gtk.ScrolledWindow()
    scroll.set_size_request(500, 400)
    scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    str = '<span font_desc="Times New Roman Bold 48" foreground="#ff0000" font_family="Times New Roman\
">Connection\nTimed Out</span>'
    (attr, text, char) = pango.parse_markup(str, accel_marker = u'\x00')
    label = gtk.Label()
    label.set_attributes(attr)
    label.set_text(text)
    label.set_justify(gtk.JUSTIFY_CENTER)
    scroll.add_with_viewport(label)
    scroll.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
    return scroll

def linkClicked(unUsed, text):
    parent = unUsed.get_parent()
    while parent.__class__.__name__ != 'OutputBox': parent = parent.get_parent()
    from gui.outputGui import SuggestionSearch
    parent.__class__.link = SuggestionSearch.ENABLE
    parent.__class__.linkText = text
    gtk.main_quit()

def noDefinition(suggestion, word):
    '''
    returns a widget containing spelling suggestions
    '''
    
    scroll = gtk.ScrolledWindow()
    scroll.set_size_request(500, 400)
    scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    str = '<span font_desc="Times New Roman Bold 24" foreground="#ff0000" font_family="Times New Roman\
"><span foreground="#000000">%s\n</span><i> No Definition Found</i></span><span font_desc="Times New Roman \
16" font_family="Times New Roman">\n\nYou\'re may be searching for\n</span>' % (word)
    (attr, text, char) = pango.parse_markup(str, accel_marker = u'\x00')
    label = gtk.Label()
    label.set_attributes(attr)
    label.set_text(text)
    label.set_justify(gtk.JUSTIFY_CENTER)
    vBox = gtk.VBox()
    vBox.pack_start(label)
    link = gtk.LinkButton('')
    link.set_label(suggestion[0].lower())
    link.connect('clicked', linkClicked, link.get_label().lower())
    link.set_tooltip_text(link.get_label().lower())
    del suggestion[0]
    alignment = gtk.Alignment(0.5, 0.5, 0, 0)
    alignment.add(link)
    vBox.pack_start(alignment)
    label = gtk.Label()
    label.set_text('\n')
    vBox.pack_start(label)
    while suggestion:
        end = len(suggestion) >= 5 and 5 or len(suggestion)
        hBox = gtk.HBox(8)
        for text in suggestion[:end]:
            link = gtk.LinkButton('')
            link.set_label(text.lower())
            link.connect('clicked', linkClicked, link.get_label().lower())
            link.set_tooltip_text(link.get_label().lower())
            alignment = gtk.Alignment(0.0, 0.5, 0, 0)
            alignment.add(link)
            hBox.pack_start(alignment)
        del suggestion[:end]
        alignment = gtk.Alignment(0.0, 0.0, 1, 0)
        alignment.add(hBox)
        vBox.pack_start(alignment)
    scroll.add_with_viewport(vBox)
    scroll.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#ffffff'))
    return scroll
