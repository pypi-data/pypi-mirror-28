import requests
import json

class JsonUtil(object):
    """docstring for JsonUtil."""
    def __init__(self, base_url):
        super(JsonUtil, self).__init__()
        self.base_url = base_url

    def get_json_data(self, func_name, **kwargs):
        data = dict(kwargs)
        #data['token'] = self._token
        url = "{0}{1}/".format(self.base_url, func_name)
        r = requests.get( url, params=data)
        return r.json()

    def get_json_data_post(self, func_name, **kwargs):
        data = dict(kwargs)
        #data['token'] = self._token
        url = "{0}{1}/".format(self.base_url, func_name)
        files = {}
        if "files" in data:
            for f in data["files"]:
                files[data["files"][f].name] = data["files"][f].read()
        r = requests.post(url, data=data, files=files)
        return r.json()

    def get_json_data_json(self, func_name, **kwargs):
        data = dict(kwargs)
        #data['token'] = self._token
        url = "{0}{1}/".format(self.base_url, func_name)
        r = requests.post(url, data=json.dumps(data), headers={'Content-Type' : 'application/json'})
        return r.json()
