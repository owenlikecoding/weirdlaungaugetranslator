import tkinter as tk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk
import pyperclip
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download necessary NLTK data
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Translation map
translation_map = {
    "eer": "epar", "ock": "eyn", "wer": "pvun", "eed": "ausert", "elp": "erss", "elf": "ackau", "chee": "kali", "age": "aulik", "aft": "afns", "ied": "öd",  "ile": "ölun", "ast": "airt", "ound": "urnt", "ure": "eton", "eige": "ijech",  "iege": "ijech", "you": "tuj", "ade": "edun", "ave": "epvnor", "call": "rüpa", "erve": "etr", "een": "est", "pro": "uber", "ough": "enwi", "umb": "arpen", "ex": "alok", "ayed": "eton", "ank": "enkrek", "ole": "uchon", "cen": "sojr","ange": "anko", "have": "haket", "if": "wun", "am": "iv", "ing": "agno","in": "eun", "tab": "vanno", "ere": "elta", "ear": "egla", "tw": "tsj", "ium": "oz", "ibe": "ijen", "ace": "apts", "arm": "epa", "rce": "dzn","rse": "id", "igh": "ern", "ike": "ënk", "ous": "il", "ard": "enak","ude": "euëg", "uf": "eb", "of": "oven", "from": "ven", "or": "urr","ame": "aure", "oul": "auk", "nce": "njo", "ine": "ott", "old": "aul","ble": "prë", "ght": "rur", "ome": "eam", "ive": "ok", "ov": "oë","ke": "get", "ple": "mounn", "has": "hald", "w": "v", "alk": "ecken","irl": "inne", "ny": "ia", "py": "ia", "ty": "ia", "sy": "ia","t": "dt", "au": "ä", "u": "ü", "ai": "ey", "oo": "ou","ss": "scë", "Deo": "craig", "ot": "ar", "ea": "ahn", "ote": "eyt","oat": "uet", "sh": "sy", "af": "ap", "is": "est", "on": "ana","ei": "eyu", "ough": "ëaw", "th": "dëh", "ll": "lsker", "ial": "ek","ly": "lik", "er": "arn", "can": "cou", "ph": "uin", "end": "idel","ack": "agch", "so": "toa", "uch": "itt", "ick": "aën", "ic": "aësch", "ang": "erla", "co": "csae", "act": "apel", "acdt": "apel", "and": "oket"
}

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def process_input(sentence):
    return word_tokenize(sentence)

def tag_parts_of_speech(words):
    return pos_tag(words)

def transform_word_order(tagged_words):
    subjects, objects, verbs = [], [], []
    for word, tag in tagged_words:
        wntag = get_wordnet_pos(tag)
        if wntag == wordnet.NOUN:
            subjects.append((word, (tag, 'nominative')))
            objects.append((word, (tag, 'accusative')))
        elif wntag == wordnet.VERB:
            verbs.append((word, (tag, 'none')))
        else:
            objects.append((word, (tag, 'none')))
    return subjects + objects + verbs

def transform_grammar(tagged_words):
    case_transformations = {
        ('NN', 'nominative'): lambda word: word + 'ey',
        ('NN', 'accusative'): lambda word: word + 'et',
        ('NN', 'instrumental'): lambda word: word + 'ud',
        ('NN', 'dative'): lambda word: word + 'oge',
        ('NN', 'genitive'): lambda word: word + 'eis',
    }
    transformed_words = [] 
    for word, (tag, case) in tagged_words:
        transformation = case_transformations.get((tag, case), lambda word: word)
        transformed_words.append(transformation(word))
    return transformed_words


def translate_characters(sentence, translation_map):
    for key in translation_map:
        sentence = sentence.replace(key, translation_map[key])
    return sentence

def translate_sentence(sentence, translation_map):
    words = process_input(sentence.lower())
    tagged_words = tag_parts_of_speech(words)
    sov_words = transform_word_order(tagged_words)
    grammar_transformed_words = transform_grammar(sov_words)
    
    seen = set()
    unique_words = [x for x in grammar_transformed_words if not (x in seen or seen.add(x))]
    
    transformed_sentence = ' '.join(unique_words)
    return translate_characters(transformed_sentence, translation_map)

def translate_text():
    sentence = entry.get()
    translated_sentence = translate_sentence(sentence, translation_map)
    result_label.config(text=translated_sentence)

def copy_to_clipboard():
    translated_text = result_label.cget("text")
    pyperclip.copy(translated_text)

# Tkinter GUI Setup
window = tk.Tk()
window.title("Sentence Translator")

entry_label = tk.Label(window, text="Enter sentence:")
entry = tk.Entry(window, width=50)
translate_button = tk.Button(window, text="Translate", command=translate_text)
result_label = tk.Label(window, text="Translated sentence will appear here")
copy_button = tk.Button(window, text="Copy", command=copy_to_clipboard)

entry_label.pack()
entry.pack()
translate_button.pack()
result_label.pack()
copy_button.pack()

window.mainloop()
