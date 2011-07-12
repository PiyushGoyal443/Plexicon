'''
@author: dibyendu das

This module acts as the interface
between the input & output
'''

from gui.inputGui import InputBox, gtk
from gui.outputGui import OutputBox, ExitState, SuggestionSearch
from gui.spinner import Spinner
from gui.error import timeOut, noDefinition
from data import *

def monitor(word, language, themeIndex):
    wordDict = getDefinition(word, language)
    if wordDict is None: return timeOut()
    if language == 'en':
        from lang.english import english, design
        altDef = getAltDef(word)
        if altDef is None: return timeOut()
        synDict = getSynonym(word)
        if len(wordDict) < 4 and synDict is None and altDef == {}:
            suggestion = getSuggestion(word)
            if suggestion is None:
                return timeOut()
            return noDefinition(suggestion, word)
        return design.LayOut(english.WordInfo(wordDict, altDef, synDict), themeIndex)()
    elif language == 'bn':
        from lang.bengali import bengali, design
        image = getImage(word)
        if image is None: return timeOut()
        import re
        if re.compile(r'^Error 404.a.: Word ".*" Not Found.<BR>').search(image):
            image = getAltImage(word)
            if image is None: return timeOut()
        if len(wordDict) < 4:
            suggestion = getSuggestion(word)
            if suggestion is None: return timeOut()
            return noDefinition(suggestion, word)
        return design.LayOut(bengali.WordInfo(wordDict, image), themeIndex)()

def inputThread(themeIndex, text, language):
    searchBox = InputBox(themeIndex, text, language)
    
def spinnerThread(themeIndex, dataDict):
    if InputBox.query != '':
        dataDict['text'] = InputBox.query
        dataDict['language'] = {'en': 0, 'bn': 1}[InputBox.target]
        dataDict['widget'] = monitor(InputBox.query, InputBox.target, themeIndex)
    gtk.main_quit()
    
def run(themeIndex):
    '''
    The apllication continues to run in a
    loop until the user closes explicitely
    '''
    
    import thread
    gtk.gdk.threads_init()
    text = ''
    language = 0
    while True:
        thread.start_new_thread(inputThread, (themeIndex, text, language))
        gtk.main()

        dataDict = {}
        spinner = Spinner()
        thread.start_new_thread(spinnerThread, (themeIndex, dataDict))
        gtk.main()
        spinner.hide_all()

        if dataDict:
            text = dataDict['text']
            language = dataDict['language']
            widget = dataDict['widget']
        else: break

        result = OutputBox(widget, themeIndex)
        result.__class__.link = SuggestionSearch.DISABLE
        gtk.main()
        state = result.returnState
        linkState = result.__class__.link
        linkText = result.__class__.linkText
        result.destroy()

        if linkState == SuggestionSearch.ENABLE:
            text = linkText

        if state == ExitState.EXIT:
            break
