import http.client
import urllib.parse

import json
from json.decoder import JSONDecodeError

class BasicRESTClient:
    def _safe_json_decode(self, data):
        try:
            obj_json = json.loads(data)
            return 200, obj_json
        except JSONDecodeError:
            return -1, None

    def _do_url_encoded_post(self, api_domain, api_url, api_url_params):
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