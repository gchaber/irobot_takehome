import json
import difflib

class EnglishDictionary:
    def __init__(self):
        self._eng_dict = None
        with open('./dictionary.json') as f:
            self._eng_dict = json.load(f)

    def spell_check(self, word):
        if word.upper() in self._eng_dict:
            return True, []
        suggestions = difflib.get_close_matches(word.upper(), self._eng_dict.keys())
        return False, suggestions