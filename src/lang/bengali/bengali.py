'''
@author: dibyendu das

This is the module to store word
definition for bengali language
'''

class WordInfo:
    '''
    Stores all the information
    of a particular word
    '''

    def __init__(self, word_dict, image_data, alt_image_data):
        self.query = word_dict['query']
        self.targetLanguage = 'Bengali'
        self.sound_url = ''
        self.image = ''
        self.alt_image = ''
        self.meaning = []
        if word_dict.has_key('primaries'):
            if word_dict['primaries'][0]['type'] == 'headword':
                self.__class__.query = word_dict['primaries'][0]['terms'][0]\
                                                                    ['text']
                if len(word_dict['primaries'][0]['terms']) > 1:
                    self.sound_url = word_dict['primaries'][0]['terms'][1]\
                                                                  ['text']
                self.meaning.extend([node['terms'][0]['text'] for node in
            word_dict['primaries'][0]['entries'] if node['type'] == 'meaning'])
        import re
        if not re.compile(r'^Error 404.a.: Word ".*" Not Found.<BR>').search(
                                                               alt_image_data):
            self.alt_image = alt_image_data
        if not re.compile(r'^<!-- SHTML Wrapper - 404 Not Found -->').search(
                                                                   image_data):
            self.image = image_data