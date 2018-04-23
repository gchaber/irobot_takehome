"""@package api_tests
This package includes the API module tests
"""
from tests.test_base import Test, TestSuite
from api.rest_client import BasicRESTClient
from api.food2fork_client import Food2ForkClient

class BasicRestClientJSONDecodeTest(Test):
    TITLE = 'BasicRestClient._safe_json_decode'

    def _setup(self):
        self._client = BasicRESTClient()

    def _run_test(self):
        if self._client._safe_json_decode('{}') != (200, {}):
            return False
        if self._client._safe_json_decode('{test}') != (-1, None):
            return False
        if self._client._safe_json_decode('') != (-1, None):
            return False
        if self._client._safe_json_decode('{"a": 1234}') != (200, {'a': 1234}):
            return False
        return True

    def _tear_down(self):
        self._client = None

class BasicRestClientDoURLEncodedPostTest(Test):
    TITLE = 'BasicRestClient._do_url_encoded_post'

    API_DOMAIN = 'e1tfqyprxj.execute-api.us-east-1.amazonaws.com'
    API_URL = '/test_api_test/urlencoded_echo'

    def _setup(self):
        self._client = BasicRESTClient()

    def _run_test(self):
        test_dicts = [
            {},
            {'a': 'world', '#b': 'hel#lo'},
            {'tes$$$t': 'wor%%ld', 'c': 'wow()@#@#'}
        ]
        for test_dict in test_dicts:
            result = self._client._do_url_encoded_post(
                BasicRestClientDoURLEncodedPostTest.API_DOMAIN,
                BasicRestClientDoURLEncodedPostTest.API_URL,
                test_dict
            )
            if (200, test_dict) != result:
                print("FAILED: test_dict: %s - result: %s" % (test_dict, result,))
                return False
        return True

    def _tear_down(self):
        self._client = None

class Food2ForkClientAPIGetRecipeTest(Test):
    TITLE = 'Food2ForkClient.api_get_recipe'

    def _setup(self):
        self._client = Food2ForkClient()

    def _run_test(self):
        (resp_status, obj_data) = self._client.api_get_recipe('035865')
        if resp_status != 200:
            return False
        if 'recipe' not in obj_data or 'ingredients' not in obj_data['recipe'] or 'title' not in obj_data['recipe']:
            return False
        if '2 cups sugar' not in obj_data['recipe']['ingredients']:
            return False
        if 'The Best Chocolate Cake' != obj_data['recipe']['title']:
            return False
        (resp_status, obj_data) = self._client.api_get_recipe('xxxxxxxxx')
        if resp_status != 200 or obj_data != {'recipe': []}:
            return False
        return True

    def _tear_down(self):
        self._client = None

class Food2ForkClientAPISearchTest(Test):
    TITLE = 'Food2ForkClient.api_search'

    class Food2ForkDummyClient(Food2ForkClient):
        def _do_url_encoded_post(self, api_domain, api_url, api_url_params):
            if 'key' not in api_url_params or api_url_params['key'] == '':
                return -1, None
            if 'sort' not in api_url_params:
                return -1, None
            sorting = api_url_params['sort']
            if sorting != 'r' and sorting != 't':
                return -1, None
            return 200, {}

    def _setup(self):
        self._client = Food2ForkClientAPISearchTest.Food2ForkDummyClient()

    def _run_test(self):
        if self._client.api_search(q='', sort='r') != (200, {}):
            return False
        if self._client.api_search(q='', sort='t') != (200, {}):
            return False
        if self._client.api_search(q='broth,chicken', sort='r') != (200, {}):
            return False
        if self._client.api_search(q='broth,chicken', sort='t') != (200, {}):
            return False
        if self._client.api_search(q='', sort='x') != (-1, None):
            return False
        self._client._api_key = ''
        if self._client.api_search(q='broth,chicken', sort='r') != (-1, None):
            return False
        return True

    def _tear_down(self):
        self._client = None

class APITestSuite(TestSuite):
    TITLE = 'API Tests'
    TESTS = [
        BasicRestClientJSONDecodeTest,
        BasicRestClientDoURLEncodedPostTest,
        Food2ForkClientAPIGetRecipeTest,
        Food2ForkClientAPISearchTest
    ]