"""@package test_base
This package includes the base functionally for the test suites and tests
"""

class Test:
    """
    The base test class used for each unit test
    """
    TITLE = 'Untitled Test'

    def _setup(self):
        """
        The purpose of this is to setup the environment for the test. It will be invoked prior to _run_test()
        """
        pass

    def _run_test(self):
        """
        Run the test and determine whether or not it has passed or failed

        :return:
            True - the test passed
            False - the test failed
        """
        return False

    def _tear_down(self):
        """
        Cleanup from the test. It will be invoked after a test has completed, pass or fail.
        """
        pass

    def run_test(self):
        """
        Run the test.
        Display some helpful output to diagnosis any failures
        """
        print("Running '%s' test" % (self.TITLE,))
        self._setup()
        result = self._run_test()
        self._tear_down()
        if not result:
            print("**** Test Failed! ****")
        return result

class TestSuite:
    """
    The test suite class encapsulates a collection of related unit tests
    """
    TITLE = 'Untitled Suite'
    TESTS = []

    @classmethod
    def run_suite(cls):
        """
        Runs all tests in the test suite

        :return:
            Title of test suite, number of passing tests, total number of tests
        """
        num_success = 0
        for test in cls.TESTS:
            if test.run_test():
                num_success += 1
        return cls.TITLE, num_success, len(cls.TESTS)