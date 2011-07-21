# -*- coding: UTF-8 -*-
'''
@author: dibyenu das

This module is used to convert a text string 
to an audio file(mp3) spelling the same text
'''

from urllib import FancyURLopener
from random import choice
from threading import Thread, Condition
import copy

USER_AGENTS = ['Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Geck\
o\20071127 Firefox/2.0.0.11',
               'Opera/9.25 (Windows NT 5.1; U; en)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET C\
LR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (li\
ke Gecko) (Kubuntu)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/200\
70731 Ubuntu/dapper-security Firefox/1.5.0.12',
               'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9']

class UrlOpener(FancyURLopener):
    '''
    custom urllib class with browser headers
    '''

    version = choice(USER_AGENTS)

class FancyThread:
    '''
    thread object returns data
    on return from the thread
    '''

    def __init__(self, func, *param):
        self.__done = 0
        self.__result = None
        self.__status = 'working'
        self.__c = Condition()
        self.__t = Thread(target = self.wrapper, args = (func, param))
        self.__t.setName("FancyThread")
        self.__t.start()

    def __repr__(self):
        return '<class \'FancyThread\' at ' + hex(id(self)) + ':' \
                + self.__status + '>'

    def __call__(self):
        self.__c.acquire()
        while self.__done == 0:
            self.__c.wait()
        self.__c.release()
        result = copy.deepcopy(self.__result)
        return result

    def wrapper(self, func, param):
        self.__c.acquire()
        try:
            self.__result = func(*param)
        except:
            self.__result = "Exception raised within FancyThread"
        self.__done = 1
        self.__status = `self.__result`
        self.__c.notify()
        self.__c.release()

def fetch(text, language):
    '''
    fetch the audio data from google server
    '''

    url = "http://translate.google.com/translate_tts?tl=" + language + "&q=" \
          + text
    opener = UrlOpener()
    page = opener.open(url)
    return page.read()

def text_to_speech(text, language = 'en'):
    '''
    Takes the 'text' & 'language' as arguments &
    returns a string containing the audio data
    '''

    return FancyThread(fetch, text, language)()