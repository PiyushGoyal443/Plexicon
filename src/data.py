'''
@author: dibyendu das

This module is used to retrieve definitions,
examples, spelling suggestions etc. from
different online dictionaries. 
'''

def connect(url):
    '''
    Returns content retrieved form 
    the web or None on failure/timeout
    '''

    time_out = 8
    import urllib2
    try:
        data = urllib2.urlopen(url, timeout = time_out).read()
    except urllib2.URLError:
        return None
    return data

def get_definition(data_dict, word, target_language = 'en'):
    "get definition from google's unofficial API"

    url = "http://www.google.com/dictionary/json?callback=dict_api.callbacks.i\
d100&q=" + word + "&sl=en&tl=" + target_language + "&restrict=pr,de&client=te"
    data = connect(url)
    if data is None:
        data_dict['definition'] = data
        return
    import re
    data = re.sub(r',200,null[)]$', '',
                  re.sub(r'^dict_api[.]callbacks[.]id100[(]', '', data))
    web_definition_part = re.compile(r',"webDefinitions":.*$')
    if web_definition_part.search(data) is not None:
        data = re.sub('$', '}', web_definition_part.sub('', data))
    import json, ast
    data_dict['definition'] = json.loads(json.dumps(ast.literal_eval(data)))
    return

def get(key):
    data = ''
    for i in range(len(key)):
        data += chr(ord(key[i - 12]) + 6)
    return data

def get_synonym(data_dict, word):
    'get synonyms, antonyms from big huge thesaurus API'

    key = r",Z-U(*-+*,+($-,*%,,Y)'+V$&',X*+)"
    url = "http://words.bighugelabs.com/api/2/" + get(get(key)) + "/" \
          + word + "/json"
    data = connect(url)
    if data is None:
        data_dict['synonym'] = data
        return
    import json, ast
    data_dict['synonym'] = json.loads(json.dumps(ast.literal_eval(data)))
    return

def get_image(data_dict, word):
    'get definition in bengali in .gif image format'

    data_dict['image'] = connect("http://ovidhan.org/index.php?act=process&o="
                                 + word + "&Sec=BNG")
    return

def get_alt_image(data_dict, word):
    'get definition in bengali in .gif image format'

    data_dict['alternative image'] = connect('http://www.bdwebguide.com/dic/' +
                                             word)
    return

def get_alt_suggestion(data_dict, word):
    "get google's spelling suggestions"

    import httplib
    import xml.dom.minidom
    data = '''
        <spellrequest textalreadyclipped="0" ignoredups="0" ignoredigits="1" ignoreallcaps="1">
            <text> %s </text>
        </spellrequest>
        '''
    result = []
    connnection = httplib.HTTPSConnection("www.google.com")
    connnection.request("POST", "/tbproxy/spell?lang=en", data % word)
    dom = xml.dom.minidom.parseString(connnection.getresponse().read())
    dom_data = dom.getElementsByTagName('spellresult')[0]
    for child_node in dom_data.childNodes:
        result = child_node.firstChild.data.lower().split()
    data_dict['alternative suggestion'] = result
    return

def get_suggestion(data_dict, word):
    "get spelling suggestions from dictionary.com"

    key = r'[]e+-b]d(g-[n&i%km[\-^W+hX&h(]^VV*d^(%&bh`'
    url = "http://api-pub.dictionary.com/v001?vid=" + get(get(key)) + \
    "&q=" + word + "&type=spelling"
    data = connect(url)
    if data is None:
        data_dict['suggestion'] = data
        return
    suggestion = []
    from path import HOME_PATH
    xml_file = HOME_PATH + '/.plexicon/data/data.xml'
    data_file = open(xml_file, 'wb')
    data_file.write(data)
    data_file.close()
    from xml.dom import minidom
    xmldoc = minidom.parse(xml_file)
    if xmldoc.childNodes[0].childNodes[1].nodeName == 'bestmatch':
        suggestion.append(xmldoc.childNodes[0].childNodes[1].\
                              childNodes[1].childNodes[0].data.lower())
    for node in xmldoc.childNodes[0].childNodes[3].childNodes[1].childNodes:
        if node.nodeName == 'suggestion':
            suggestion.append(node.childNodes[0].data.lower())
    data_dict['suggestion'] = suggestion
    return

def parse_example(text, definition):
    '''parses the example sentences'''

    for example in text.split('<br>'):
        if example == '.':
            continue
        part_of_speech_tuple = example.partition(':')
        key = part_of_speech_tuple[0].rstrip()
        import re
        if re.compile(r'[(].*[)]').search(key) is not None:
            key = re.sub(r'[(].*[)]', '', key).rstrip()
        if definition.has_key(key):
            if part_of_speech_tuple[2]:
                definition[key]['example'] = []
                for text in part_of_speech_tuple[2].split('<ex>,</ex>'):
                    definition[key]['example'].append(text.strip())

def get_example(data_dict, word):

    key = r'[]e+-b]d(g-[n&i%km[\-^W+hX&h(]^VV*d^(%&bh`'
    url = "http://api-pub.dictionary.com/v001?vid=" + get(get(key)) + \
    "&q=" + word + "&type=example"
    data_dict['example'] = connect(url)
    return

def get_alt_def(data_dict, word):
    'get alternative definition from dictionary.com'

    key = r'[]e+-b]d(g-[n&i%km[\-^W+hX&h(]^VV*d^(%&bh`'
    url = "http://api-pub.dictionary.com/v001?vid=" + get(get(key)) + \
    "&q=" + word + "&type=define"
    data = connect(url)
    if data is None:
        data_dict['alternative definition'] = data
        return
    from path import HOME_PATH
    xml_file = HOME_PATH + '/.plexicon/data/data.xml'
    data_file = open(xml_file, 'wb')
    data_file.write(data)
    data_file.close()
    from xml.dom import minidom
    xmldoc = minidom.parse(xml_file)
    node = xmldoc.getElementsByTagName('dictionary')
    if node[0].attributes[node[0].attributes.keys()[1]].value == '0':
        data_dict['alternative definition'] = {}
        return
    def_dict = {}
    entry_list = xmldoc.getElementsByTagName('entry')
    for entry_node in entry_list:
        part_of_speech_list = entry_node.getElementsByTagName('partofspeech')
        for partofspeech_node in part_of_speech_list:
            text = partofspeech_node.attributes[partofspeech_node.attributes.\
                                               keys()[0]].value.lower()
            import re
            if re.compile(r'[(].*[)]').search(text) is not None:
                text = re.sub(r' .*$', '', re.sub(r'[(].*[)]', '', text))
            if text == 'verb phrase':
                if not def_dict.has_key(text):
                    def_dict[text] = {}
                key = entry_node.getElementsByTagName('display_form')[0].\
                                                      firstChild.data
                if entry_node.getElementsByTagName('var') != []:
                    key += ' / ' + entry_node.getElementsByTagName('var')[0].\
                                                      firstChild.data
                if not def_dict[text].has_key(key):
                    def_dict[text][key] = []
                def_list = partofspeech_node.getElementsByTagName('def')
                for definition in def_list:
                    def_dict[text][key].append(definition.firstChild.data)
            elif text == "idiom":
                if not def_dict.has_key(text):
                    def_dict[text] = {}
                key = entry_node.getElementsByTagName('display_form')[0].\
                                                      firstChild.data
                if entry_node.getElementsByTagName('var') != []:
                    key += ' / ' + entry_node.getElementsByTagName('var')[0].\
                                                      firstChild.data
                if not def_dict[text].has_key(key):
                    def_dict[text][key] = []
                def_list = partofspeech_node.getElementsByTagName('def')
                for definition in def_list:
                    def_dict[text][key].append(definition.firstChild.data)
            else:
                if not def_dict.has_key(text):
                    def_dict[text] = {}
                    def_dict[text]['meaning'] = []
                def_list = partofspeech_node.getElementsByTagName('def')
                for definition in def_list:
                    def_dict[text]['meaning'].append(definition.firstChild.data)
    data_dict['alternative definition'] = def_dict
    return