import json

import requests


class HttpUtil:

    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None, headers=None, timeout=10):
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Get Request Error: {e}")
            return None

    def post(self, url, data=None, headers=None, timeout=10):
        try:
            response = self.session.post(url, data=data, headers=headers, timeout=timeout)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print(f"POST Request Error: {e}")
            return None

