import tkinter as tk
import pyperclip
from nltk.tokenize import word_tokenize

# Original translation map
translation_map = {
       "eer": "epar", "ock": "eyn", "wer": "pvun", "eed": "ausert", "elp": "erss", "elf": "ackau", "chee": "kali", "age": "aulik", "aft": "afns", "ied": "öd",  "ile": "ölun", "ast": "airt", "ound": "urnt", "ure": "eton", "eige": "ijech",  "iege": "ijech", "you": "tuj", "ade": "edun", "ave": "epvnor", "call": "rüpa", "erve": "etr", "een": "est", "pro": "uber", "ough": "enwi", "umb": "arpen", "ex": "alok", "ayed": "eton", "ank": "enkrek", "ole": "uchon", "cen": "sojr","ange": "anko", "have": "haket", "if": "wun", "am": "iv", "ing": "agno","in": "eun", "tab": "vanno", "ere": "elta", "ear": "egla", "tw": "tsj", "ium": "oz", "ibe": "ijen", "ace": "apts", "arm": "epa", "rce": "dzn","rse": "id", "igh": "ern", "ike": "ënk", "ous": "il", "ard": "enak","ude": "euëg", "uf": "eb", "of": "oven", "from": "ven", "or": "urr","ame": "aure", "oul": "auk", "nce": "njo", "ine": "ott", "old": "aul","ble": "prë", "ght": "rur", "ome": "eam", "ive": "ok", "ov": "oë","ke": "get", "ple": "mounn", "has": "hald", "w": "v", "alk": "ecken","irl": "inne", "ny": "ia", "py": "ia", "ty": "ia", "sy": "ia","t": "dt", "au": "ä", "u": "ü", "ai": "ey", "oo": "ou","ss": "scë", "Deo": "craig", "ot": "ar", "ea": "ahn", "ote": "eyt","oat": "uet", "sh": "sy", "af": "ap", "is": "est", "on": "ana","ei": "eyu", "ough": "ëaw", "th": "dëh", "ll": "lsker", "ial": "ek","ly": "lik", "er": "arn", "can": "cou", "ph": "uin", "end": "idel","ack": "agch", "so": "toa", "uch": "itt", "ick": "aën", "ic": "aësch", "ang": "erla", "co": "csae", "act": "apel", "acdt": "apel", "and": "oket" 
 }

# Reverse the translation map
reversed_translation_map = {v: k for k, v in translation_map.items()}

# Reversed grammar suffixes
grammar_suffixes = ['ey', 'et', 'ud', 'oge', 'eis']

def process_input(sentence):
    return word_tokenize(sentence)

def revert_grammar(words):
    reverted_words = []
    for word in words:
        for suffix in grammar_suffixes:
            if word.endswith(suffix):
                word = word[:-len(suffix)]
                break
        reverted_words.append(word)
    return reverted_words

def revert_characters(words, reversed_map):
    reverted_sentence = ' '.join(words)
    for key in reversed_map:
        reverted_sentence = reverted_sentence.replace(key, reversed_map[key])
    return reverted_sentence

def untranslate_sentence(sentence, reversed_map):
    words = process_input(sentence.lower())
    grammar_reverted_words = revert_grammar(words)
    return revert_characters(grammar_reverted_words, reversed_map)

def untranslate_text():
    sentence = entry.get()
    untranslated_sentence = untranslate_sentence(sentence, reversed_translation_map)
    result_label.config(text=untranslated_sentence)

def copy_to_clipboard():
    untranslated_text = result_label.cget("text")
    pyperclip.copy(untranslated_text)

# Tkinter GUI Setup for Untranslator
window = tk.Tk()
window.title("Sentence Untranslator")

entry_label = tk.Label(window, text="Enter sentence in fictional language:")
entry = tk.Entry(window, width=50)
untranslate_button = tk.Button(window, text="Untranslate", command=untranslate_text)
result_label = tk.Label(window, text="Untranslated sentence will appear here")
copy_button = tk.Button(window, text="Copy", command=copy_to_clipboard)

entry_label.pack()
entry.pack()
untranslate_button.pack()
result_label.pack()
copy_button.pack()

window.mainloop()
