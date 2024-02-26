import tkinter as tk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk
import pyperclip

# Download necessary NLTK data
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')

# Translation map
translation_map = {
    "eer": "epar", "hello": "Helskau", " i ": " iy ", " ire ": " iy ", " pie ": " tret ", "remember": "betäk", "ouse": "äs", " my ": " mär ", " me ": " mä ", "had": "behaln", "'s": " thrä", "sing": "zëng", "sang": "zëng", "play": "späl",  "soldier": "saldattar", "war ": "krag ", "battle": "siyge", "big": "grüt", "just": "nähr", "est": "wä", "by ": "nëben ", "with ": "mëdst ", "people": "vülka", "yes": "jah", "we ": "vir ", "down": "änder", "under": "änder", "money": "gäller", "to ": "tejil ", "own": "unt", "did": "enod", "stop": "held", "what": "wath", "die": "starur", "death": "starn", "dead": "staren",  "low": "lä", "art": "arte", "ock": "eyn", "see": "sern", "were": "voë", "when": "nean", "who": "hun", "why": "vöre", "eed": "ause", "elp": "erss",
    "elf": "ackär", "chee": "kali", "ance": "anz", "age": "aulik", "aft": "afns", "ied": "öd",
    "ile": "ölun", "ast": "irst", "ound": "urnt", "ure": "erun", "eige": "ijech",
    "iege": "ijech", "you": "tuj", "ade": "edun", "ave": "epvnor", "call": "rüpa",
    "erve": "etr", "een": "est", "pro": "de", "ough": "enwi", "umb": "arpen",
    "ex": "aloc", "ayed": "eton", "ank": "enkrek", "ole": "ucon", "cen": "sojr",
    "ange": "anko", "have": "haket", "if": "wun", "am": "iv", "ing": "ande",
    "in": "eun", "tab": "vanno", "ere": "ene", "ear": "oö", "tw": "tsj",
    "ium": "oz", "ibe": "ijen", "ace": "apts", "arm": "era", "rce": "dzn",
    "rse": "id", "igh": "ern", "ike": "ënk", "ous": "il", "ard": "enak",
    "ude": "euëg", "uf": "eb", "of": "oven", "from": "ven", "or": "urr",
    "ame": "aure", "oul": "auk", "nce": "nell", "ine": "ott", "old": "aul",
    "ble": "prë", "ght": "rur", "ome": "eam", "ive": "ok", "ov": "oë",
    "ke": "get", "ple": "vä", "has": "hald", "wa": "veu", "alk": "eckan",
    "irl": "inne", "ny": "ia", "py": "ia", "ty": "ia", "country": "lënde", "nation": "vülgelönde", "sy": "ia",
    "et": "edt", "au": "ä", "u": "ü", "air": "läft", "oo": "ou",
    "ss": "scë", "craig": "DEYO", "ot": "aär", "rea": "renu", "ote": "eyt",
    "oat": "uet", "sh": "sc", "af": "ap", "is": "ens", "on": "ana",
    "ei": "eyu", "ough": "ëaw", "th": "dëh", "ll": "lsker", "ial": "ek",
    "ly": "lik", "can": "cö", "ph": "fo", "end": "idel",
    "ack": "agch", "sou": "si", "clean": "soor", "uch": "itt", "ick": "aën", "ic": "aësch", "ang": "erla", "cow": "cuu", "act": "apel", "acdt": "apel", "and ": "oket ", "are ": "sud ", "does": "enne", "peak": "prog", "its": "esk", "know": "weute", "little": "clien", "how": "weag", "new": "naä",
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
        (wordnet.NOUN, 'nominative'): lambda word: word + 'ers',
        (wordnet.NOUN, 'accusative'): lambda word: word + 're',
        (wordnet.NOUN, 'instrumental'): lambda word: word + 'ud',
        (wordnet.NOUN, 'dative'): lambda word: word + 'oge',
        (wordnet.NOUN, 'genitive'): lambda word: word + 'eis',
        (wordnet.VERB, 'none'): lambda word: word + 'e',
    }
    transformed_words = []   
    for word, (tag, case) in tagged_words:
        wntag = get_wordnet_pos(tag)
        transformation = case_transformations.get((wntag, case), lambda word: word)
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