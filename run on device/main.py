import tkinter as tk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk

# Ensure that NLTK can download datasets over HTTPS
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
    "eer": "epar", "ock": "eyn", "wer": "pvun", "eed": "ausert", "elp": "erss",
    "elf": "ackau", "chee": "kali", "age": "aulik", "aft": "afns", "ied": "öd",
    "ile": "ölun", "ast": "airt", "ound": "urnt", "ure": "eton", "eige": "ijech",
    "iege": "ijech", "you": "tuj", "ade": "edun", "ave": "epvnor", "call": "rüpa",
    "erve": "etr", "een": "est", "pro": "uber", "ough": "enwi", "umb": "arpen",
    "ex": "alok", "ayed": "eton", "ank": "enkrek", "ole": "uchon", "cen": "sojr",
    "ange": "anko", "have": "haket", "if": "wun", "am": "iv", "ing": "ande",
    "in": "eun", "tab": "vanno", "ere": "ene", "ear": "egla", "tw": "tsj",
    "ium": "oz", "ibe": "ijen", "ace": "apts", "arm": "era", "rce": "dzn",
    "rse": "id", "igh": "ern", "ike": "ënk", "ous": "il", "ard": "enak",
    "ude": "euëg", "uf": "eb", "of": "oven", "from": "ven", "or": "urr",
    "ame": "aure", "oul": "auk", "nce": "njo", "ine": "ott", "old": "aul",
    "ble": "prë", "ght": "rur", "ome": "eam", "ive": "ok", "ov": "oë",
    "ke": "get", "ple": "mounn", "has": "hald", "wa": "veu", "alk": "ecken",
    "irl": "inne", "ny": "ia", "py": "ia", "ty": "ia", "sy": "ia",
    "et": "edt", "au": "ä", "u": "ü", "ai": "ey", "oo": "ou",
    "ss": "scë", "Deo": "craig", "ot": "ar", "rea": "renu", "ote": "eyt",
    "oat": "uet", "sh": "sy", "af": "ap", "is": "ens", "on": "ana",
    "ei": "eyu", "ough": "ëaw", "th": "dëh", "ll": "lsker", "ial": "ek",
    "ly": "lik", "er": "arn", "can": "cou", "ph": "uin", "end": "idel",
    "ack": "agch", "sou": "si", "clean": "soor", "uch": "itt", "ick": "aën", "ic": "aësch", "ang": "erla", "co": "csae", "act": "apel", "acdt": "apel", "and": "oket", "are": "sud", "does": "enne", "peak": "prog", "its": "esk", "know": "weute", "little": "clien"
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

def transform_grammar(tagged_words):
    transformed = []
    for word, tag in tagged_words:
        wntag = get_wordnet_pos(tag)
        transformed_word = translation_map.get(word, word) # Default to original word if not in map
        transformed.append(transformed_word)
    return transformed

def translate_sentence(sentence):
    words = process_input(sentence)
    tagged_words = tag_parts_of_speech(words)
    transformed_words = transform_grammar(tagged_words)
    return ' '.join(transformed_words)

# GUI setup
root = tk.Tk()
root.title("Sentence Translator")

input_label = tk.Label(root, text="Enter Sentence:")
input_label.pack()

input_text = tk.Entry(root, width=50)
input_text.pack()

output_label = tk.Label(root, text="Translated Sentence:")
output_label.pack()

output_text = tk.Entry(root, width=50)
output_text.pack()

def on_translate():
    input_sentence = input_text.get()
    translated_sentence = translate_sentence(input_sentence)
    output_text.delete(0, tk.END)
    output_text.insert(0, translated_sentence)

translate_button = tk.Button(root, text="Translate", command=on_translate)
translate_button.pack()

root.mainloop()
