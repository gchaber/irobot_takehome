"""@package user_interface_tests
This package includes the UI state machine and text processing tests
"""
from tests.test_base import Test, TestSuite
from takehome import TakeHomeApplication, TakeHomeAppState, UnknownTakeHomeAppStateException

class InvalidTakeHomeAppStateTest(Test):
    TITLE = 'InvalidTakeHomeAppState'

    def _setup(self):
        self._app = TakeHomeApplication()

    def _run_test(self):
        self._app._state = 90
        try:
            self._app._process_state()
        except UnknownTakeHomeAppStateException as e:
            if str(e) != 'Invalid State':
                print("%s != Invalid State" % (str(e)))
                return False
        self._app._state = TakeHomeAppState.TEST_UNIMPLEMENTED
        try:
            self._app._process_state()
        except UnknownTakeHomeAppStateException as e:
            if str(e) != 'Unimplemented State':
                print("%s != Unimplemented State" % (str(e)))
                return False
        return True

    def _tear_down(self):
        self._app = None

class TakeHomeApplicationDummy(TakeHomeApplication):
    def __init__(self):
        super(TakeHomeApplicationDummy, self).__init__()
        self.get_numeric_selection_result = 1
        self.split_input_result = []

    def _get_numeric_selection(self, max_sel):
        return self.get_numeric_selection_result

    def _split_input(self, prompt_text):
        return self.split_input_result

class StateTest(Test):
    def _setup(self):
        self._app = TakeHomeApplicationDummy()

    def _tear_down(self):
        self._app = None

class TakeHomeAppErrorStateTest(StateTest):
    TITLE = 'TakeHome AppState - ERROR state'

    def _run_test(self):
        self._app._state = TakeHomeAppState.ERROR
        self._app._error_message = "Testing Error State"
        if not self._app._process_state():
            return False
        if self._app.app_state() != TakeHomeAppState.FINISHED:
            return False
        return True

class TakeHomeAppFinishedStateTest(StateTest):
    TITLE = 'TakeHome AppState - FINISHED state'

    def _run_test(self):
        self._app._state = TakeHomeAppState.FINISHED
        if self._app._process_state():
            return False
        return True

class TakeHomeAppEnterIngredientStateTest(StateTest):
    TITLE = 'TakeHome AppState - ENTER_INGREDIENT state'

    def _run_test(self):
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            print("self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT (1)")
            return False
        self._app.split_input_result = ['flour']
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK (1)")
            return False
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            print("self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT (2)")
            return False
        self._app.split_input_result = ['butter']
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK (2)")
            return False
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            print("self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT (3)")
            return False
        self._app.split_input_result = ['cream', 'of', 'tartar']
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK (2)")
            return False
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            print("self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT (3)")
            return False
        self._app.split_input_result = []
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.API_SEARCH:
            print("self._app.app_state() != TakeHomeAppState.API_SEARCH (1)")
            return False
        if self._app._curr_ingredients != ['flour', 'butter', 'cream of tartar']:
            print("self._app._curr_ingredients != ['flour', 'butter', 'cream of tartar',]")
            return False
        return True

class TakeHomeAppSpellingSuggestionStateTest(StateTest):
    TITLE = 'TakeHome AppState - SPELL_CHECK_SUGGESTIONS state'

    def _run_test(self):
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            print("self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT (1)")
            return False
        self._app.split_input_result = ['oange']
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK (1)")
            return False
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK_SUGGESTIONS:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK_SUGGESTIONS (1)")
            return False
        # Invalid selection
        self._app.get_numeric_selection_result = -1
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK_SUGGESTIONS:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK_SUGGESTIONS (2)")
            return False
        # Choose first (original option)
        self._app.get_numeric_selection_result = 1
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            print("self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT (2)")
            return False
        self._app.split_input_result = ['flur']
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK (2)")
            return False
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.SPELL_CHECK_SUGGESTIONS:
            print("self._app.app_state() != TakeHomeAppState.SPELL_CHECK_SUGGESTIONS (2)")
            return False
        # Reenter Ingredient
        self._app.get_numeric_selection_result = len(self._app._spelling_suggestions)+1
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            print("self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT (3)")
            return False
        self._app.split_input_result = []
        self._app._process_state()
        if self._app.app_state() != TakeHomeAppState.API_SEARCH:
            print("self._app.app_state() != TakeHomeAppState.API_SEARCH")
            return False
        if self._app._curr_ingredients != ['oange']:
            print("self._app._curr_ingredients != ['oange']")
            return False
        return True

class TakeHomeAppElaboratePossibilitiesTest(Test):
    TITLE = 'TakeHomeApplication._elaborate_possibilities'

    def _setup(self):
        self._app = TakeHomeApplication()

    def _run_test(self):
        self._app._spelling_suggestions = []
        self._app._elaborate_possibilities([['peanut', 'cocoa'], ['butter', 'something']])
        if self._app._spelling_suggestions != ['peanut butter', 'peanut something', 'cocoa butter', 'cocoa something']:
            return False
        return True

    def _tear_down(self):
        self._app = None

class TakeHomeAppIsIngredientInCurrTest(Test):
    TITLE = 'TakeHomeApplication._is_ingredient_in_curr'

    def _setup(self):
        self._app = TakeHomeApplication()

    def _run_test(self):
        self._app._curr_ingredients = ['butter', 'cream']
        if not self._app._is_ingredient_in_curr('1/2 stick of butter'):
            return False
        if not self._app._is_ingredient_in_curr('1 cup of   cream'):
            return False
        if self._app._is_ingredient_in_curr('1/2 cup of milk'):
            return False
        return True

    def _tear_down(self):
        self._app = None

class TakeHomeAppWaitAPIAttemptsTest(Test):
    TITLE = 'TakeHomeApplication._wait_api_attempts'

    def _setup(self):
        self._app = TakeHomeApplication()
        self._saved_timeout = TakeHomeApplication.RETRY_WAIT_TIMEOUT
        TakeHomeApplication.RETRY_WAIT_TIMEOUT = 0.1

    def _run_test(self):
        self._app._api_attempts = 2
        self._app._wait_api_attempts()
        if self._app.app_state() != TakeHomeAppState.ENTER_INGREDIENT:
            return False
        self._app._wait_api_attempts()
        if self._app.app_state() != TakeHomeAppState.ERROR:
            return False
        return True

    def _tear_down(self):
        TakeHomeApplication.RETRY_WAIT_TIMEOUT = self._saved_timeout
        self._app = None

class UserInterfaceTestSuite(TestSuite):
    TITLE = 'User Interface/State Machine Tests'
    TESTS = [
        InvalidTakeHomeAppStateTest,
        TakeHomeAppErrorStateTest,
        TakeHomeAppFinishedStateTest,
        TakeHomeAppEnterIngredientStateTest,
        TakeHomeAppSpellingSuggestionStateTest,
        TakeHomeAppElaboratePossibilitiesTest,
        TakeHomeAppIsIngredientInCurrTest,
        TakeHomeAppWaitAPIAttemptsTest
    ]