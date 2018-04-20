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
    results = []
    if test == 'api' or test == 'all':
        results.append(APITestSuite.run_suite())
    if test == 'spellcheck' or test == 'all':
        results.append(SpellCheckTestSuite.run_suite())
    if test == 'user_interface' or test == 'all':
        results.append(UserIntefaceTestSuite.run_suite())
    print("Test Report")
    for (suite_title, num_success, total_tests) in results:
        print("%s: Pass/Total: %s/%s" % (suite_title, num_success, total_tests,))

if __name__ == '__main__':
    main(sys.argv[1:])