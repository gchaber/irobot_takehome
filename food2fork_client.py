from rest_client import BasicRESTClient
import json

class Food2ForkClient(BasicRESTClient):
    API_DOMAIN = 'food2fork.com'
    API_SEARCH_URL = '/api/search'
    API_GET_RECIPE_URL = '/api/get'

    def __init__(self):
        self._api_key = None
        with open('./credentials.json') as f:
            cred_dict = json.load(f)
            if 'food2fork_api_key' not in cred_dict:
                raise KeyError("No api key present - make sure you set the food2fork_api_key in credentials.json")
            self._api_key = cred_dict['food2fork_api_key']

    def _create_cred_params(self):
        return {'key': self._api_key}

    def api_search(self, q=None, sort=None, page=None):
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
        api_url_params = self._create_cred_params()
        api_url_params['rId'] = rId
        return self._do_url_encoded_post(Food2ForkClient.API_DOMAIN,
                                         Food2ForkClient.API_GET_RECIPE_URL,
                                         api_url_params)
