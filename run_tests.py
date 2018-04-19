import sys
from tests.api import APITestSuite
from tests.spellcheck import SpellCheckTestSuite
from tests.user_interface import UserIntefaceTestSuite

def main(args):
    if len(args) != 1:
        print("Invalid number of arguments")
        print("Usage: python3 run_tests.py <test>")
        print("test: all, api, spellcheck, user_interface")
        return
    test = args[0]
    if test == 'api' or test == 'all':
        APITestSuite.run_suite()
    if test == 'spellcheck' or test == 'all':
        SpellCheckTestSuite.run_suite()
    if test == 'user_interface' or test == 'all':
        UserIntefaceTestSuite.run_suite()

if __name__ == '__main__':
    main(sys.argv[1:])