'''
@author: dibyendu das

This module creates widgets containing error messages
on network timeout[via time_out() function] or on not
finding any valid definition [via no_definition() function]
'''

import gtk, pango

def time_out():
    '''
    this function is called 
    when network times out
    '''

    scroll = gtk.ScrolledWindow()
    scroll.set_size_request(500, 400)
    scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    string = '<span font_desc="Times New Roman Bold 48" foreground="#ff0000" f\
ont_family="Times New Roman">Connection\nInterrupted</span>'
    (attr, text, unused) = pango.parse_markup(string, accel_marker = u'\x00')
    label = gtk.Label()
    label.set_attributes(attr)
    label.set_text(text)
    label.set_justify(gtk.JUSTIFY_CENTER)
    alignment = gtk.Alignment(0, 0, 1, 1)
    alignment.add(label)
    scroll.add_with_viewport(alignment)
    scroll.get_child().modify_bg(gtk.STATE_NORMAL,
                                 gtk.gdk.color_parse('#ffffff'))
    return scroll

def linked(link, text):
    'called when link button is clicked'

    parent = link.get_parent()
    while parent.__class__.__name__ != 'OutputBox':
        parent = parent.get_parent()
    from gui.OutputGui import SuggestionSearch
    parent.__class__.link = SuggestionSearch.ENABLE
    parent.__class__.linkText = text
    gtk.main_quit()

def no_definition(suggestion, word):
    '''
    returns a widget containing spelling suggestions
    '''

    scroll = gtk.ScrolledWindow()
    scroll.set_size_request(500, 400)
    scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    string = '<span font_desc="Times New Roman Bold 24" foreground="#ff0000" f\
ont_family="Times New Roman"><span foreground="#000000">%s\n</span><i> No Defi\
nition Found</i></span><span font_desc="Times New Roman 16" font_family="Times\
 New Roman">\n\nMay be you\'re searching for\n</span>' % (word)
    (attr, text, unused) = pango.parse_markup(string, accel_marker = u'\x00')
    label = gtk.Label()
    label.set_attributes(attr)
    label.set_text(text)
    label.set_justify(gtk.JUSTIFY_CENTER)
    v_box = gtk.VBox()
    v_box.pack_start(label)
    link = gtk.LinkButton('')
    link.set_label(suggestion[0].lower())
    link.connect('clicked', linked, link.get_label().lower())
    link.set_tooltip_text('click to search')
    del suggestion[0]
    alignment = gtk.Alignment(0.5, 0.5, 0, 0)
    alignment.add(link)
    v_box.pack_start(alignment)
    label = gtk.Label()
    label.set_text('\n')
    v_box.pack_start(label)
    while suggestion:
        end = len(suggestion) >= 5 and 5 or len(suggestion)
        h_box = gtk.HBox(8)
        for text in suggestion[:end]:
            link = gtk.LinkButton('')
            link.set_label(text.lower())
            link.connect('clicked', linked, link.get_label().lower())
            link.set_tooltip_text('click to search')
            alignment = gtk.Alignment(0.0, 0.5, 0, 0)
            alignment.add(link)
            h_box.pack_start(alignment)
        del suggestion[:end]
        alignment = gtk.Alignment(0.0, 0.0, 1, 0)
        alignment.add(h_box)
        v_box.pack_start(alignment)
    scroll.add_with_viewport(v_box)
    scroll.get_child().modify_bg(gtk.STATE_NORMAL,
                                 gtk.gdk.color_parse('#ffffff'))
    return scroll