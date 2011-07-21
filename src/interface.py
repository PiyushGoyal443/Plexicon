'''
@author: dibyendu das

This module acts as the interface
between the input & output
'''

import pygtk
pygtk.require('2.0')
from gui.InputGui import InputBox, gtk
from gui.OutputGui import OutputBox, ExitState, SuggestionSearch
from gui.spinner import Spinner
from gui.error import time_out, no_definition
from data import get_definition, get_alt_def, get_synonym
from data import get_suggestion, get_image, get_alt_image

def monitor(word, language, theme_index):
    'fetches the apt layout for the output interface'

    word_dict = get_definition(word, language)
    if word_dict is None:
        return time_out()
    if language == 'en':
        from lang.english import english, design
        alternative_definition = get_alt_def(word)
        if alternative_definition is None:
            return time_out()
        synonym_dict = get_synonym(word)
        if len(word_dict) < 4 and synonym_dict is None and \
           alternative_definition == {}:
            suggestion = get_suggestion(word)
            if suggestion is None:
                return time_out()
            return no_definition(suggestion, word)
        return design.LayOut(english.WordInfo(word_dict,
                        alternative_definition, synonym_dict), theme_index)()
    elif language == 'bn':
        from lang.bengali import bengali, design
        image = get_image(word)
        if image is None:
            return time_out()
        import re
        if re.compile(r'^Error 404.a.: Word ".*" Not Found.<BR>').search(image):
            image = get_alt_image(word)
            if image is None:
                return time_out()
        if len(word_dict) < 4:
            suggestion = get_suggestion(word)
            if suggestion is None:
                return time_out()
            return no_definition(suggestion, word)
        return design.LayOut(bengali.WordInfo(word_dict, image), theme_index)()

def input_thread(theme_index, text, language, editable):
    'input interface is handled by this thread'

    InputBox(theme_index, text, language, editable)

def spinner_thread(theme_index, data_dict):
    'spinner object is activated in this thread'

    if InputBox.query != '':
        data_dict['text'] = InputBox.query
        data_dict['language'] = {'en': 0, 'bn': 1}[InputBox.target]
        data_dict['widget'] = monitor(InputBox.query,
                                      InputBox.target, theme_index)
    gtk.main_quit()

def run(theme_index):
    '''
    The application continues to run in a
    loop until the user closes explicitly
    '''

    import thread
    gtk.gdk.threads_init()
    text = ''
    language = 0
    editable = True
    while True:
        thread.start_new_thread(input_thread, (theme_index, text, language,
                                               editable))
        gtk.main()

        data_dict = {}
        spinner = Spinner()
        thread.start_new_thread(spinner_thread, (theme_index, data_dict))
        gtk.main()
        spinner.hide_all()

        if data_dict:
            text = data_dict['text']
            language = data_dict['language']
            widget = data_dict['widget']
            editable = True
        else: break

        result = OutputBox(widget, theme_index)
        result.__class__.link = SuggestionSearch.DISABLE
        gtk.main()
        state = result.returnState
        link_state = result.__class__.link
        link_text = result.__class__.linkText
        result.destroy()

        if link_state == SuggestionSearch.ENABLE:
            text = link_text
            editable = False
        if state == ExitState.EXIT:
            break