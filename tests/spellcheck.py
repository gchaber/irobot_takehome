"""@package spellcheck_tests
This package includes the spellcheck module tests
"""
from tests.test_base import Test, TestSuite
from spellcheck.english_dict import EnglishDictionary

class EnglishDictionarySpellCheckTest(Test):
    TITLE = 'EnglishDictionary.spell_check'

    def _setup(self):
        self._eng_dict = EnglishDictionary()

    def _run_test(self):
        if self._eng_dict.spell_check('home') != (True, 'home', []):
            return False
        if self._eng_dict.spell_check('test') != (True, 'test', []):
            return False
        if self._eng_dict.spell_check('cream') != (True, 'cream', []):
            return False
        if self._eng_dict.spell_check('suga') != (False, 'suga', ['sugar', 'sug', 'sura']):
            return False
        if self._eng_dict.spell_check('flor') != (False, 'flor', ['fluor', 'flour', 'flora']):
            return False
        if self._eng_dict.spell_check('wonderfull') != (False, 'wonderfull', ['wonderful', 'wonderly', 'overfull']):
            return False
        return True

    def _tear_down(self):
        self._eng_dict = None

class SpellCheckTestSuite(TestSuite):
    TITLE = 'Spell Check/English Dictionary Tests'
    TESTS = [
        EnglishDictionarySpellCheckTest
    ]