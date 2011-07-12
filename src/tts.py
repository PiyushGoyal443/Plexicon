# -*- coding: UTF-8 -*-
'''
@author: dibyenu das

This module is used to convert a text string 
to an audio file(mp3) spelling the same text
'''

from urllib import FancyURLopener
from random import choice
from threading import *
import copy

user_agents = ['Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
               'Opera/9.25 (Windows NT 5.1; U; en)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
               'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
               'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9']

class UrlOpener(FancyURLopener):
    version = choice(user_agents)

class FancyThread:

    def __init__(self, func, *param):
        self.__done = 0
        self.__result = None
        self.__status = 'working'
        self.__C = Condition()
        self.__T = Thread(target = self.wrapper, args = (func, param))
        self.__T.setName("FancyThread")
        self.__T.start()

    def __repr__(self):
        return '<class \'FancyThread\' at ' + hex(id(self)) + ':' + self.__status + '>'

    def __call__(self):
        self.__C.acquire()
        while self.__done == 0:
            self.__C.wait()
        self.__C.release()
        a = copy.deepcopy(self.__result)
        return a

    def wrapper(self, func, param):
        self.__C.acquire()
        try:
            self.__result = func(*param)
        except:
            self.__result = "Exception raised within FancyThread"
        self.__done = 1
        self.__status = `self.__result`
        self.__C.notify()
        self.__C.release()

def fetch(text, language):
    url = "http://translate.google.com/translate_tts?tl=" + language + "&q=" + text
    opener = UrlOpener()
    page = opener.open(url)
    return page.read()

def textToSpeech(text, language = 'en'):
    '''
    Takes the 'text' & 'language' as arguments &
    returns a string containing the audio data
    '''
    return FancyThread(fetch, text, language)()
