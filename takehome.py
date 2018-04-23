"""@package takehome
This package contains the main application
"""
from api.food2fork_client import Food2ForkClient
from spellcheck.english_dict import EnglishDictionary
from enum import Enum
import time

class TakeHomeAppState(Enum):
    """
    All of the possible application states, details for each can be found in the TakeHomeApplication class documentation
    """
    TEST_UNIMPLEMENTED = -1
    ERROR = 0
    FINISHED = 1
    ENTER_INGREDIENT = 2
    SPELL_CHECK = 3
    SPELL_CHECK_SUGGESTIONS = 4
    API_SEARCH_SORTING = 5
    API_SEARCH = 6
    API_GET_RECIPE = 7
    DISPLAY_RESULTS = 8

class UnknownTakeHomeAppStateException(Exception):
    pass

class TakeHomeApplication:
    """
    This class is responsible for implementing the main application/handling the user flow
    """
    MAX_API_ATTEMPTS = 4
    RETRY_WAIT_TIMEOUT = 5

    def app_state(self):
        """
        Accessor function for self._state
        :return:
            App state
        """
        return self._state

    def __init__(self):
        """
        Constructor

        Initializes the Food2Fork client, spell check dictionary and state
        Initial State: ENTER_INGREDIENT
        """
        self._food2fork_client = Food2ForkClient()
        self._spell_checker = EnglishDictionary()

        self._state_func_map = {
            TakeHomeAppState.ERROR:                     self._state_on_error,
            TakeHomeAppState.ENTER_INGREDIENT:          self._state_enter_ingredient,
            TakeHomeAppState.SPELL_CHECK:               self._state_spell_check,
            TakeHomeAppState.SPELL_CHECK_SUGGESTIONS:   self._state_spell_check_suggestions,
            TakeHomeAppState.API_SEARCH_SORTING:        self._state_api_search_sorting,
            TakeHomeAppState.API_SEARCH:                self._state_api_search,
            TakeHomeAppState.API_GET_RECIPE:            self._state_api_get_recipe,
            TakeHomeAppState.DISPLAY_RESULTS:           self._state_display_results
        }
        self._state = TakeHomeAppState.ENTER_INGREDIENT

        self._curr_ingredients = []
        self._spelling_suggestions = []
        self._entered_ingredient = []
        self._sorting = ''
        self._api_attempts = -1
        self._error_message = ''
        self._recipe_id = ''
        self._recipe_title = ''
        self._recipe_f2f_url = ''

    def _elaborate_possibilities(self, packed_suggestions, possibility=''):
        """
        This function will recursively create suggestions for the spelling of the entire ingredient based on the individual suggestions of each word.

        PRECONDITION: self._spelling_suggestions = [] (This function fills this array)

        :param packed_suggestions:
            The array of suggestions for the spelling of each word in the ingredient
        :param possibility:
            The current formed suggestion that, when complete, represents a suggestion of the spelling of the entire ingredient
        """
        if len(packed_suggestions) == 0:
            self._spelling_suggestions.append(possibility)
            return
        head_suggestions = packed_suggestions[0]
        if possibility != '':
            possibility += ' '
        for suggestion in head_suggestions:
            self._elaborate_possibilities(packed_suggestions[1:], possibility + suggestion)

    def _is_ingredient_in_curr(self, ingredient):
        """
        This function checks to see if the recipe's ingredient was one of the supplied ingredients
        :param ingredient:
            the recipe ingredient to check
        :return:
            True - is the ingredient
            False - is not the ingredient
        """
        for curr_ingredient in self._curr_ingredients:
            if ingredient.find(curr_ingredient) != -1:
                return True
        return False

    def _get_numeric_selection(self, max_sel):
        """
        This function get a numeric selection from the user.
        The minimum choice is always 1.

        :param max_sel:
            The maximum choice number
        :return:
        """
        sel = input("Enter selection: ")
        if not sel.isdigit():
            print("Invalid selection, must be a number")
            return -1
        sel = int(sel)
        if sel < 1 or sel > max_sel:
            print("Invalid selection, must be between 1 and %s" % (max_sel,))
            return -1
        return sel

    def _split_input(self, prompt_text):
        """
        This function abstracts the input function and tokenizes the input into a list of words.
        :param prompt_text:
            The prompt given to the user
        :return:
            list representing the tokenized input
        """
        return input(prompt_text).split()

    def _wait_api_attempts(self):
        """
        This function waits for RETRY_WAIT_TIMEOUT seconds and then decrements the self._api_attempts variable
        If it reaches 0, it transitions to the ERROR state.
        Otherwise, it continues on in the current state.
        """
        time.sleep(TakeHomeApplication.RETRY_WAIT_TIMEOUT)
        self._api_attempts -= 1
        if self._api_attempts == 0:
            self._error_message = 'Maximum API attempts exceeded'
            self._state = TakeHomeAppState.ERROR

    def _process_state(self):
        """
        This function properly calls the correct state handler function.
        Descriptions for each state can be found in the handlers.

        :return:
            True - Application is finished
            False - Keep going

            raises UnknownTakeHomeStateException if state is invalid or unimplemented
        """
        if not isinstance(self._state, TakeHomeAppState):
            raise UnknownTakeHomeAppStateException('Invalid State')
        elif self._state == TakeHomeAppState.FINISHED:
            return False
        elif self._state not in self._state_func_map:
            raise UnknownTakeHomeAppStateException('Unimplemented State')
        self._state_func_map[self._state]()
        return True

    def _state_enter_ingredient(self):
        """
        ENTER_INGREDIENT state handler function

        This state is responsible for getting an ingredient from the user.
        It will properly validate the input, making sure that it is made up of words (isalpha)
        If it fails validation, it will stay in this state until it doesn't

        Next, it will transition to:
            API_SEARCH_SORTING - if no input is entered
            SPELL_CHECK - if valid input is entered
        """
        self._entered_ingredient = self._split_input("Enter single ingredient (leave blank if done): ")
        if len(self._entered_ingredient) == 0:
            self._state = TakeHomeAppState.API_SEARCH_SORTING
            return
        if False not in [x.isalpha() for x in self._entered_ingredient]:
            self._state = TakeHomeAppState.SPELL_CHECK
            return
        print("Invalid input")

    def _state_spell_check(self):
        """
        SPELL_CHECK state handler function

        This state is responsible for checking the spelling of the ingredient.
        It will check each word in the ingredient. If no words are misspelled, then it will:
            1. Add the ingredient to the list
            2. Return back to the ENTER_INGREDIENT state
        If any word is possibly misspelled, it will form a list of possibilities given the list of suggestions for each misspelled word in the ingredient
        It will then transition to the SPELL_CHECK_SUGGESTIONS state to allow the user to choose from this list
        """
        spelling_results = [self._spell_checker.spell_check(word) for word in self._entered_ingredient]
        packed_suggestions = []
        for (correct, word, suggestions) in spelling_results:
            if correct:
                packed_suggestions.append([word])
            else:
                packed_suggestions.append([word] + suggestions)
        self._spelling_suggestions = []
        self._elaborate_possibilities(packed_suggestions)
        if len(self._spelling_suggestions) == 1:
            self._curr_ingredients.append(self._spelling_suggestions[0])
            self._state = TakeHomeAppState.ENTER_INGREDIENT
            return
        self._state = TakeHomeAppState.SPELL_CHECK_SUGGESTIONS

    def _state_spell_check_suggestions(self):
        """
        SPELL_CHECK_SUGGESTIONS state handler function

        After the list of suggestions is formed for the spelling of the entire ingredient, this state:
            1. Prints them out, including a selection to reenter
            2. Prompts user for input
            3. Validates the input
        If it fails to validate, it will stay in this state and make the user try again.
        Otherwise, it will transition back to the ENTER_INGREDIENT state
        """
        print("Not sure if you spelled the ingredient correctly? Choose from below:")
        i = 1
        for suggestion in self._spelling_suggestions:
            print("%s. %s" % (i, suggestion,))
            i += 1
        print("%s. Reenter ingredient" % (i,))
        sel = self._get_numeric_selection(i)
        if sel == -1:
            return
        if sel != i:
            self._curr_ingredients.append(self._spelling_suggestions[sel-1])
        self._state = TakeHomeAppState.ENTER_INGREDIENT

    def _state_api_search_sorting(self):
        """
        API_SEARCH_SORTING state handler function

        This state determines from user input what kind of sorting the user will like to base the recipe selection on
        If validation succeeds, it transitions to the API_SEARCH state
        Otherwise, it keeps asking until valid input is entered
        """
        print("Would you like to find the best recipe by:")
        print("1. Rating")
        print("2. Trendingness")
        sel = self._get_numeric_selection(2)
        if sel == 1:
            self._sorting = 'r'
        else:
            self._sorting = 't'
        self._state = TakeHomeAppState.API_SEARCH
        self._api_attempts = TakeHomeApplication.MAX_API_ATTEMPTS

    def _state_api_search(self):
        """
        API_SEARCH state handler function

        This state queries Food2Fork for a recipe that contains the supplied ingredients
        It allows for MAX_API_ATTEMPTS if there's an error with the request, waits RETRY_WAIT_TIMEOUT between tries
        Validates the response, making sure there's a recipe
        If there is no recipe or another error, it stops here and goes to the ERROR state
        Otherwise, it grabs the top recipe's id and transitions to the API_GET_RECIPE state
        """
        comma_sep_list = ''
        for ingredient in self._curr_ingredients:
            comma_sep_list += ingredient + ','
        comma_sep_list = comma_sep_list[:-1]
        resp_status, obj_data = self._food2fork_client.api_search(q=comma_sep_list, sort=self._sorting)
        if resp_status != 200 or obj_data is None:
            print("API Search Failed, status: %s, retrying in %s seconds" % (resp_status,
                                                                             TakeHomeApplication.RETRY_WAIT_TIMEOUT))
            self._wait_api_attempts()
            return
        if 'recipes' not in obj_data or len(obj_data['recipes']) == 0 or 'recipe_id' not in obj_data['recipes'][0]:
            self._error_message = 'No recipe returned, you must have had some interesting ingredients'
            self._state = TakeHomeAppState.ERROR
            return
        self._recipe_id = obj_data['recipes'][0]['recipe_id']
        self._api_attempts = TakeHomeApplication.MAX_API_ATTEMPTS
        self._state = TakeHomeAppState.API_GET_RECIPE

    def _state_api_get_recipe(self):
        """
        API_GET_RECIPE state handler function

        This state retrieves the full recipe from Food2Fork.
        The purpose is to find the full list of ingredients and compare that against the supplied

        It allows for MAX_API_ATTEMPTS if there's an error with the request, waits RETRY_WAIT_TIMEOUT between tries
        Validates the response and if there is another error, it stops here and goes to the ERROR state
        Otherwise, it transitions to the DISPLAY_RESULTS state
        """
        resp_status, obj_data = self._food2fork_client.api_get_recipe(self._recipe_id)
        if resp_status != 200 or obj_data is None:
            print("API Get Recipe Failed, status: %s, retrying in %s seconds" % (resp_status,
                                                                                 TakeHomeApplication.RETRY_WAIT_TIMEOUT))
            self._wait_api_attempts()
            return
        if 'recipe' not in obj_data or \
           'ingredients' not in obj_data['recipe'] or \
           'title' not in obj_data['recipe'] or \
           'f2f_url' not in obj_data['recipe']:
            self._error_message = "The recipe information did not get returned for some reason"
            self._state = TakeHomeAppState.ERROR
            return
        self._recipe_ingredients = obj_data['recipe']['ingredients']
        self._recipe_title = obj_data['recipe']['title']
        self._recipe_f2f_url = obj_data['recipe']['f2f_url']
        self._state = TakeHomeAppState.DISPLAY_RESULTS

    def _state_display_results(self):
        """
        DISPLAY_RESULTS state handler function

        Displays the ingredients that aren't in the supplied ingredients
        Then, it transitions to the FINISHED state
        """
        print("Recipe Title: %s" % (self._recipe_title,))
        print("Food2Fork URL: %s" % (self._recipe_f2f_url,))

        print("Supplied ingredients:")
        if len(self._curr_ingredients) == 0:
            print("None")
        else:
            for ingredient in self._curr_ingredients:
                print("%s" % (ingredient,))
        print("")
        print("Recipe ingredients that weren't supplied:")
        at_least_one = False
        for ingredient in self._recipe_ingredients:
            if not self._is_ingredient_in_curr(ingredient):
                at_least_one = True
                print("%s" % (ingredient,))
        if not at_least_one:
            print("None")
        self._state = TakeHomeAppState.FINISHED

    def _state_on_error(self):
        """
        ERROR state handler function

        Prints the error text and transitions to the FINISHED state
        """
        print("Error: %s" % (self._error_message,))
        self._state = TakeHomeAppState.FINISHED

    def main(self):
        """
        Entry point of application

        The application will continue until self._process_state() returns False
        """
        while self._process_state():
            pass

if __name__ == '__main__':
    app = TakeHomeApplication()
    app.main()