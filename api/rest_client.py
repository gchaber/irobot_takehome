"""@package rest_client
This package includes a basic REST client
"""
import http.client
import urllib.parse

import json
from json.decoder import JSONDecodeError

class BasicRESTClient:
    """
    This class provides basic functionally for a REST client using http.client
    """
    def _safe_json_decode(self, data):
        """
        This function safely decodes a JSON string into an object.
        Since this function is only used when the response code is 200, it returns 200 if successful.
        If bad JSON is provided, the response status will be -1 and the dict will be None

        :param data:
            the JSON string that comes from the HTTP response

        :return:
            response status, response dict
        """
        try:
            obj_json = json.loads(data)
            return 200, obj_json
        except JSONDecodeError:
            return -1, None

    def _do_url_encoded_post(self, api_domain, api_url, api_url_params):
        """
        This function performs a 'POST' request with a urlencoded body.

        :param api_domain:
            the domain of the request (e.g. www.google.com)

        :param api_url:
            the endpoint path (e.g. /api/endpoint)

        :param api_url_params:
            a dictionary of URL parameters to be encoded

        :return:
            response status, response dict
        """
        params = urllib.parse.urlencode(api_url_params)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        conn = http.client.HTTPSConnection(api_domain)
        conn.request("POST", api_url, params, headers)
        response = conn.getresponse()
        if response.status != 200:
            return response.status, response.reason
        data = response.read()
        conn.close()
        return self._safe_json_decode(data)