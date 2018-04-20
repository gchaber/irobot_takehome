class Test:
    TITLE = 'Untitled Test'

    def _setup(self):
        pass

    def _test(self):
        return False

    def _tear_down(self):
        pass

    def run_test(self):
        print("Running '%s' test" % (self.TITLE,))
        self._setup()
        result = self._test()
        self._tear_down()
        print("Test Succeeded: %s" % (result,))
        return result

class TestSuite:
    TITLE = 'Untitled Suite'
    TESTS = []

    @classmethod
    def run_suite(cls):
        num_success = 0
        for test in cls.TESTS:
            if test.run_test():
                num_success += 1
        return cls.TITLE, num_success, len(cls.TESTS)