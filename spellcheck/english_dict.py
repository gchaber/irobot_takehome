"""@package english_dict
This package includes the EnglishDictionary class
"""
import json
import difflib

class EnglishDictionary:
    """
    This class provides spell checking with suggestions if a word is misspelled
    """
    def __init__(self):
        """
        Constructor function

        Loads the 'dictionary.json' file and initializes self._eng_dict to the parsed contents in the file.

        Exceptions:
            raises JSONDecodeError if file is not a valid JSON string
            raises FileNotFoundError if file is not present
        """
        self._eng_dict = None
        with open('./dictionary.json') as f:
            self._eng_dict = json.load(f)

    def spell_check(self, word):
        """
        This function provides spell checking on a single word

        :param word:
            The word to spell check. It is case insensitive

        :return:
            Correct spelling - True, empty list
            Incorrect spelling - False, list containing suggestions (lowercase).
        """
        if word.upper() in self._eng_dict:
            return True, []
        suggestions = [x.lower() for x in difflib.get_close_matches(word.upper(), self._eng_dict.keys())]
        return False, suggestions