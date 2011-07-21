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

    query = ''
    targetLanguage = 'Bengali'
    def __init__(self, word_dict, image_data):
        self.sound_url = ''
        self.image = ''
        self.meaning = []
        self.__class__.query = word_dict['query']
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
        if not re.compile(r'^<!-- SHTML Wrapper - 404 Not Found -->').search(
                                                                   image_data):
            self.image = image_data