'''
@author: dibyendu das

This is the module to store
everything like definition,
spelling suggestion, example,
synonym, antonym etc. in
the following two classes
for english language
'''

class PartOfSpeechInfo:
    '''
    This class parses the data retrieved
    from web & maintains information related 
    to a particular part of speech in english
    '''

    def __getTerms(self, list):
        word = partOfSpeech = url = ''
        phonetic = []
        for node in list:
            if node['type'] == "text":
                word = node['text'].capitalize()
                if node.has_key('labels'):
                    if node['labels'][0]['title'] == 'Part-of-speech':
                        partOfSpeech = node['labels'][0]['text'].capitalize()
            elif node['type'] == 'sound':
                url = node['text']
            else:
                phonetic.append(node['text'])
        return (partOfSpeech, word, url, phonetic)

    def __getEntries(self, list):
        for item in list :
            if item['type'] == 'related':
                self.related = [(node['labels'][0]['text'], node['text']) for node in item['terms']]
            elif item['type'] == 'meaning' :
                if len(item) == 2 :
                    self.meaning[item['terms'][0]['text']] = ['', ]
                else :
                    self.meaning[item['terms'][0]['text']] = [node['terms'][0]['text'] for node in item['entries']]

    def __init__(self, word, altDef, synonym, key = None, query = None):
        self.word = self.partOfSpeech = self.soundUrl = ''
        self.phonetic = []
        self.synonym = []
        self.antonym = []
        self.related = []
        self.meaning = {}
        if word is None and synonym is None:
            self.word = query.capitalize()
            self.partOfSpeech = key.capitalize()
            if key == 'idiom' or key == 'verb phrase':
                for definition in altDef[key].keys():
                    self.meaning[definition] = []
                    for example in altDef[key][definition]:
                        self.meaning[definition].append(example)
            else:
                for definition in altDef[key]:
                    self.meaning[definition] = ['', ]
            del altDef[key]
        elif word is None and synonym is not None:
            self.word = query.capitalize()
            self.partOfSpeech = key.capitalize()
            if synonym[key].has_key('ant'):
                self.antonym = synonym[key]['ant']
            if synonym[key].has_key('syn'):
                self.synonym = synonym[key]['syn']
            if synonym[key].has_key('sim'):
                self.synonym.extend(synonym[key]['sim'])
            if altDef != {}:
                if altDef.has_key(key):
                    for definition in altDef[key]:
                        self.meaning[definition] = ['', ]
                    del altDef[key]
            del synonym[key]
        else:
            if word['type'] == "headword":
                (self.partOfSpeech, self.word, self.soundUrl, self.phonetic) = self.__getTerms(word['terms'])
                self.__getEntries(word['entries'])
            key = self.partOfSpeech.lower()
            if synonym is not None:
                if synonym.has_key(key):
                    if synonym[key].has_key('ant'):
                        self.antonym = synonym[key]['ant']
                    if synonym[key].has_key('syn'):
                        self.synonym = synonym[key]['syn']
                    if synonym[key].has_key('sim'):
                        self.synonym.extend(synonym[key]['sim'])
                    del synonym[key]
            if altDef != {}:
                if altDef.has_key(key):
                    for definition in altDef[key]:
                        self.meaning[definition] = ['', ]
                    del altDef[key]

class WordInfo:
    '''
    Stores all the information
    of a particular word
    '''
    
    query = ''
    targetLanguage = 'English'
    partsOfSpeeches = []
    def __init__(self, wordDict, altDefinition, synDict):
        self.__class__.query = wordDict['query']
        if not wordDict.has_key('primaries'):
            if synDict is None:
                if altDefinition != {}:
                    self.partsOfSpeeches = [PartOfSpeechInfo(None, altDefinition, None, key, self.query)
                                             for key in altDefinition.keys()]
            else:
                self.partsOfSpeeches = [PartOfSpeechInfo(None, altDefinition, synDict, key, self.query)
                                             for key in synDict.keys()]
                if altDefinition != {}:
                    self.partsOfSpeeches.extend([PartOfSpeechInfo(None, altDefinition, None, key, self.query)
                                             for key in altDefinition.keys()])
        else:
            if synDict is None:
                self.partsOfSpeeches = [PartOfSpeechInfo(dict, altDefinition, None) for dict in wordDict['primaries']]
                if altDefinition != {}:
                    self.partsOfSpeeches.extend([PartOfSpeechInfo(None, altDefinition, None, key, self.query)
                                             for key in altDefinition.keys()])
            else:
                self.partsOfSpeeches = [PartOfSpeechInfo(dict, altDefinition, synDict) for dict in wordDict['primaries']]
                if synDict != {}:
                    self.partsOfSpeeches.extend([PartOfSpeechInfo(None, altDefinition, synDict, key, self.query)
                                            for key in synDict.keys()])
                if altDefinition != {}:
                    self.partsOfSpeeches.extend([PartOfSpeechInfo(None, altDefinition, None, key, self.query)
                                            for key in altDefinition.keys()])
