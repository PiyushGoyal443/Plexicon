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
    def __init__(self, wordDict, imageData):
        self.soundUrl = ''
        self.image = ''
        self.meaning = []
        self.__class__.query = wordDict['query']
        if wordDict.has_key('primaries'):
            if wordDict['primaries'][0]['type'] == 'headword':
                self.__class__.query = wordDict['primaries'][0]['terms'][0]['text']
                self.soundUrl = wordDict['primaries'][0]['terms'][1]['text']
                self.meaning.extend([node['terms'][0]['text'] for node in wordDict['primaries'][0]['entries'] if node['type'] == 'meaning'])
        import re
        if not re.compile(r'^<!-- SHTML Wrapper - 404 Not Found -->').search(imageData):
            self.image = imageData
