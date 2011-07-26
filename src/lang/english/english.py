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

    def __get_terms(self, data_list):
        'used solely to parse data fetched from google'

        word = part_of_speech = url = ''
        phonetic = []
        for node in data_list:
            if node['type'] == "text":
                word = node['text'].capitalize()
                if node.has_key('labels'):
                    if node['labels'][0]['title'] == 'Part-of-speech':
                        part_of_speech = node['labels'][0]['text'].capitalize()
            elif node['type'] == 'sound':
                url = node['text']
            else:
                phonetic.append(node['text'])
        return (part_of_speech, word, url, phonetic)

    def __get_entries(self, data_list):
        'used to parse data fetched from google'

        for item in data_list :
            if item['type'] == 'related':
                self.related = [(node['labels'][0]['text'], node['text'])
                                for node in item['terms']]
            elif item['type'] == 'meaning' :
                if len(item) == 2 :
                    self.meaning[item['terms'][0]['text']] = ['', ]
                else :
                    self.meaning[item['terms'][0]['text']] = [node['terms'][0]
                                         ['text'] for node in item['entries']]

    def __init__(self, word, alt_def, synonym, key = None, query = None):
        self.word = self.part_of_speech = self.sound_url = ''
        self.phonetic = []
        self.synonym = []
        self.antonym = []
        self.related = []
        self.example = []
        self.meaning = {}
        if word is None and synonym is None:
            self.word = query.capitalize()
            self.part_of_speech = key.capitalize()
            if key == 'idiom' or key == 'verb phrase':
                for definition in alt_def[key].keys():
                    self.meaning[definition] = []
                    for example in alt_def[key][definition]:
                        self.meaning[definition].append(example)
            else:
                for definition in alt_def[key]['meaning']:
                    self.meaning[definition] = ['', ]
                if alt_def[key].has_key('example'):
                    self.example.extend(alt_def[key]['example'])
            del alt_def[key]
        elif word is None and synonym is not None:
            self.word = query.capitalize()
            self.part_of_speech = key.capitalize()
            if synonym[key].has_key('ant'):
                self.antonym = synonym[key]['ant']
            if synonym[key].has_key('syn'):
                self.synonym = synonym[key]['syn']
            if synonym[key].has_key('sim'):
                self.synonym.extend(synonym[key]['sim'])
            if alt_def != {}:
                if alt_def.has_key(key):
                    for definition in alt_def[key]['meaning']:
                        self.meaning[definition] = ['', ]
                    if alt_def[key].has_key('example'):
                        self.example.extend(alt_def[key]['example'])
                    del alt_def[key]
            del synonym[key]
        else:
            if word['type'] == "headword":
                (self.part_of_speech, self.word, self.sound_url,
                 self.phonetic) = self.__get_terms(word['terms'])
                self.__get_entries(word['entries'])
            key = self.part_of_speech.lower()
            if synonym is not None:
                if synonym.has_key(key):
                    if synonym[key].has_key('ant'):
                        self.antonym = synonym[key]['ant']
                    if synonym[key].has_key('syn'):
                        self.synonym = synonym[key]['syn']
                    if synonym[key].has_key('sim'):
                        self.synonym.extend(synonym[key]['sim'])
                    del synonym[key]
            if alt_def != {}:
                if alt_def.has_key(key):
                    for definition in alt_def[key]['meaning']:
                        self.meaning[definition] = ['', ]
                    if alt_def[key].has_key('example'):
                        self.example.extend(alt_def[key]['example'])
                    del alt_def[key]

class WordInfo:
    '''
    Stores all the information
    of a particular word
    '''

    def __init__(self, word_dict, alt_definition, syn_dict):
        self.query = word_dict['query']
        self.targetLanguage = 'English'
        self.parts_of_speeches = []
        if not word_dict.has_key('primaries'):
            if syn_dict is None:
                if alt_definition != {}:
                    self.parts_of_speeches = [PartOfSpeechInfo(None,
       alt_definition, None, key, self.query) for key in alt_definition.keys()]
            else:
                self.parts_of_speeches = [PartOfSpeechInfo(None,
         alt_definition, syn_dict, key, self.query) for key in syn_dict.keys()]
                if alt_definition != {}:
                    self.parts_of_speeches.extend([PartOfSpeechInfo(None,
      alt_definition, None, key, self.query) for key in alt_definition.keys()])
        else:
            if syn_dict is None:
                self.parts_of_speeches = [PartOfSpeechInfo(word_dictionary,
           alt_definition, None) for word_dictionary in word_dict['primaries']]
                if alt_definition != {}:
                    self.parts_of_speeches.extend([PartOfSpeechInfo(None,
      alt_definition, None, key, self.query) for key in alt_definition.keys()])
            else:
                self.parts_of_speeches = [PartOfSpeechInfo(word_dictionary,
       alt_definition, syn_dict) for word_dictionary in word_dict['primaries']]
                if syn_dict != {}:
                    self.parts_of_speeches.extend([PartOfSpeechInfo(None,
        alt_definition, syn_dict, key, self.query) for key in syn_dict.keys()])
                if alt_definition != {}:
                    self.parts_of_speeches.extend([PartOfSpeechInfo(None,
      alt_definition, None, key, self.query) for key in alt_definition.keys()])