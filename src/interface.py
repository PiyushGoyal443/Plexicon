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
from gui.favourite import Favourite
from gui.error import time_out, no_definition
from data import get_definition, get_alt_def, get_image, get_example, \
parse_example, get_suggestion, get_synonym, get_alt_image, get_alt_suggestion
from database import DataBase
import thread

def check_web_data(web_dict, language, flags):
    'fetches all sorts of definitions from the web servers'

    if language == 'en':
        if web_dict.has_key('definition') and web_dict.has_key('synonym') and \
           web_dict.has_key('alternative definition')and not web_dict.has_key(
                                                                    'example'):
            if flags[0]:
                flags[1] = False
                return False
    else:
        if web_dict.has_key('definition') and web_dict.has_key('image') \
           and web_dict.has_key('alternative image'):
            flags[1] = False
            return False
    return True

def parse(web_dict, flags):
    'merges the examples with the alternative definitions'

    if web_dict.has_key('alternative definition') and \
       web_dict.has_key('example'):
        if web_dict['example']:
            from xml.dom import minidom
            xmldoc = minidom.parseString(web_dict['example'])
            for node in xmldoc.getElementsByTagName('example'):
                text = node.childNodes[0].data
                parse_example(text, web_dict['alternative definition'])
        del web_dict['example']
        flags[0] = True
        return False
    return True

def check_suggestion(web_dict, flag):
    '''
    compares & merges selectively the two
    suggestion lists fetched from two servers
    '''

    if web_dict.has_key('suggestion') and web_dict.has_key(
                                                'alternative suggestion'):
        if not web_dict['suggestion']:
            flag[1] = False
            return False
        best_match = set()
        if web_dict['alternative suggestion']:
            best_match = set([web_dict['alternative suggestion'][0]])
            del web_dict['alternative suggestion'][0]
        if web_dict['suggestion']:
            best_match.add(web_dict['suggestion'][0])
            del web_dict['suggestion'][0]
        alt_suggestion = set(web_dict['alternative suggestion'])
        suggestion = set(web_dict['suggestion'])
        suggestion = alt_suggestion.union(suggestion)
        for word in list(best_match):
            suggestion.discard(word)
        web_dict.clear()
        web_dict['suggestion'] = []
        web_dict['suggestion'].extend(list(best_match))
        web_dict['suggestion'].extend(list(suggestion))
        flag[1] = False
        return False
    return True

def fetch_from_web(word, language, theme_index):
    'fetches the apt layout for the output interface'

    import gobject
    web_dict = {}
    flags = [False, True]
    thread.start_new_thread(get_definition, (web_dict, word, language))
    if language == 'en':
        from lang.english import english, design
        thread.start_new_thread(get_alt_def, (web_dict, word))
        thread.start_new_thread(get_example, (web_dict, word))
        thread.start_new_thread(get_synonym, (web_dict, word))
        gobject.timeout_add(160, check_web_data, web_dict, language, flags)
        gobject.timeout_add(40, parse, web_dict, flags)
        while flags[1]:
            pass
        if not web_dict['alternative definition'] and \
           not web_dict['definition']:
            return time_out()
        if len(web_dict['definition']) < 4 and web_dict['synonym'] is None \
           and web_dict['alternative definition'] == {}:
            web_dict.clear()
            flags[1] = True
            thread.start_new_thread(get_suggestion, (web_dict, word))
            thread.start_new_thread(get_alt_suggestion, (web_dict, word))
            gobject.timeout_add(80, check_suggestion, web_dict, flags)
            while flags[1]:
                pass
            if web_dict['suggestion'] is None:
                return time_out()
            return no_definition(web_dict['suggestion'], word)
        return design.LayOut(english.WordInfo(web_dict['definition'],
                             web_dict['alternative definition'],
                             web_dict['synonym']), theme_index)()
    elif language == 'bn':
        from lang.bengali import bengali, design
        thread.start_new_thread(get_image, (web_dict, word))
        thread.start_new_thread(get_alt_image, (web_dict, word))
        gobject.timeout_add(160, check_web_data, web_dict, language, flags)
        while flags[1]:
            pass
        if not web_dict['definition']:
            return time_out()
        if len(web_dict['definition']) < 4:
            web_dict.clear()
            flags[1] = True
            thread.start_new_thread(get_suggestion, (web_dict, word))
            thread.start_new_thread(get_alt_suggestion, (web_dict, word))
            gobject.timeout_add(80, check_suggestion, web_dict, flags)
            while flags[1]:
                pass
            if web_dict['suggestion'] is None:
                return time_out()
            return no_definition(web_dict['suggestion'], word)
        return design.LayOut(bengali.WordInfo(web_dict['definition'],
                            web_dict['image'], web_dict['alternative image']),
                            theme_index)()

def fetch_from_database(row, language, theme_index):
    '''
    fetches the WordInfo object corresponding
    to the word from the database
    '''

    import pickle
    word = pickle.loads(str(row[{'en': 1, 'bn': 2}[language]]))
    if language == 'en':
        from lang.english import design
        return design.LayOut(word, theme_index, True)()
    else:
        from lang.bengali import design
        return design.LayOut(word, theme_index, True)()


def input_thread(theme_index, text, language):
    'input interface is handled by this thread'

    InputBox(theme_index, text, language)

def spinner_thread(theme_index, data_dict):
    'spinner object is activated in this thread'

    if InputBox.query != '':
        data_dict['text'] = InputBox.query
        data_dict['language'] = {'en': 0, 'bn': 1}[InputBox.target]
        table = (len(InputBox.query) > 1 and InputBox.query[1] != ' ') and \
                                  InputBox.query[:2] or InputBox.query[:1]
        database = DataBase()
        row = database.select_row(table, InputBox.query)
        if not row or not row[{'en': 1, 'bn': 2}[InputBox.target]]:
            data_dict['widget'] = fetch_from_web(InputBox.query,
                                        InputBox.target, theme_index)
        else:
            data_dict['widget'] = fetch_from_database(row, InputBox.target,
                                                      theme_index)
    gtk.main_quit()

def linked(link, favourite , database_search):
    'called when link button is clicked'

    favourite.hide(called_by_link = True)
    database_search['enable'] = True
    database_search['text'] = link.get_label().lower()
    return False

def page_set_thread(page_dict, index, favourite, database_search):
    'each such 26 threads will create the 26 pages of the notebook'

    h_box = gtk.HBox(False, 20)
    v_box = gtk.VBox()
    h_box.pack_start(v_box)
    table = chr(ord('a') + index)
    database = DataBase()
    count = 0
    if database.row_count(table):
        words = database.select(table)
        count += 1
        link = gtk.LinkButton('')
        link.set_label(words[0][0])
        link.connect('clicked', linked, favourite, database_search)
        link.set_tooltip_text('click to search')
        alignment = gtk.Alignment(0, 0.5, 0, 0)
        alignment.add(link)
        v_box.pack_start(alignment)
    for number in range(26):
        if database.row_count(table + chr(ord('a') + number)):
            words = database.select(table + chr(ord('a') + number))
            for word in words:
                count += 1
                link = gtk.LinkButton('')
                link.set_label(word[0])
                link.connect('clicked', linked, favourite, database_search)
                link.set_tooltip_text('click to search')
                alignment = gtk.Alignment(0, 0.5, 0, 0)
                alignment.add(link)
                v_box.pack_start(alignment)
                if count >= 25:
                    count -= 25
                    alignment = gtk.Alignment(0, 0, 0, 0)
                    v_box = gtk.VBox()
                    alignment.add(v_box)
                    h_box.pack_start(alignment)
    database.close()
    alignment = gtk.Alignment(0, 0, 0, 0)
    alignment.add(h_box)
    scroll = gtk.ScrolledWindow()
    scroll.set_size_request(400, 400)
    scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scroll.add_with_viewport(alignment)
    scroll.get_child().modify_bg(gtk.STATE_NORMAL,
                                 gtk.gdk.color_parse('#ffffff'))
    page_dict[chr(ord('A') + index)] = scroll
    return

def create_notebook(notebook, favourite, database_search):
    'creates a notebook widget having 26 pages'

    book = gtk.Notebook()
    book.set_tab_pos(gtk.POS_TOP)
    book.set_scrollable(True)
    book.popup_enable()
    notebook.append(book)
    page_dict = {}
    notebook.append(page_dict)
    for index in range(26):
        thread.start_new_thread(page_set_thread, (page_dict, index, favourite,
                                                  database_search))
    return

def run(theme_index):
    '''
    The application continues to run in a
    loop until the user closes explicitly
    '''

    gtk.gdk.threads_init()
    text = ''
    language = 0
    skip_input = False
    database_search = {'enable':False, 'text':''}
    notebook = []
    favourite = Favourite()
    create_notebook(notebook, favourite, database_search)
    while True:
        if not skip_input:
            thread.start_new_thread(input_thread, (theme_index, text,
                                                   language))
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
        else: break
        result = OutputBox(widget, theme_index, notebook, favourite)
        result.__class__.link = SuggestionSearch.DISABLE
        gtk.main()
        result.destroy()
        if database_search['enable']:
            database_search['enable'] = False
            InputBox.query = database_search['text']
            skip_input = True
            continue
        state = result.returnState
        link_state = result.__class__.link
        link_text = result.__class__.linkText
        if link_state == SuggestionSearch.ENABLE:
            InputBox.query = link_text
            skip_input = True
            continue
        if state == ExitState.RESTART:
            skip_input = False
        else: break
