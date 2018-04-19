"""@package food2fork_client
This package includes the Food2Fork API Client
"""
from api.rest_client import BasicRESTClient
import json

class Food2ForkClient(BasicRESTClient):
    """
    This class provides basic functionally to communicate to the Food2Fork APIs.
    It supports the 'search' and 'get' endpoints.
    An api key must be provided in 'credentials.json' under 'food2fork_api_key'

    Details on the exact responses, go to https://food2fork.com/about/api
    """
    API_DOMAIN = 'food2fork.com'
    API_SEARCH_URL = '/api/search'
    API_GET_RECIPE_URL = '/api/get'

    def __init__(self):
        """
        Constructor function

        Loads the 'credentials.json' file and initializes self._api_key to the 'food2fork_api_key' stored in the file.

        Exceptions:
            raises KeyError if parameter is not present
            raises FileNotFoundError if file is not present
        """
        self._api_key = None
        with open('./credentials.json') as f:
            cred_dict = json.load(f)
            if 'food2fork_api_key' not in cred_dict:
                raise KeyError("No api key present - make sure you set the food2fork_api_key in credentials.json")
            self._api_key = cred_dict['food2fork_api_key']

    def _create_cred_params(self):
        """
        This function builds the initial URL parameters dictionary containing the authentication parameters used in every request

        :return:
            dict containing authentication parameters for a request to Food2Fork
        """
        return {'key': self._api_key}

    def api_search(self, q=None, sort=None, page=None):
        """
        Performs a search of the Food2Fork recipe database

        :param q: (Optional)
            A comma separated string of ingredients to require in the recipe

        :param sort: (Optional) Two values
            r - sort by rating
            t - sort by trendingness

        :param page: (Optional)
            The default maximum per page is 30, to receive beyond this, specify the page number

        :return:
            response status, response dict
        """
        api_url_params = self._create_cred_params()
        if q:
            api_url_params['q'] = q
        if sort:
            api_url_params['sort'] = sort
        if page:
            api_url_params['page'] = page
        return self._do_url_encoded_post(Food2ForkClient.API_DOMAIN,
                                         Food2ForkClient.API_SEARCH_URL,
                                         api_url_params)

    def api_get_recipe(self, rId):
        """
        Retrieves a recipe by id

        :param rId:
            The recipe identifier

        :return:
            response status, response dict
        """
        api_url_params = self._create_cred_params()
        api_url_params['rId'] = rId
        return self._do_url_encoded_post(Food2ForkClient.API_DOMAIN,
                                         Food2ForkClient.API_GET_RECIPE_URL,
                                         api_url_params)
