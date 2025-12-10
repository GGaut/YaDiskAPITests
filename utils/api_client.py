import requests

from configs.config import OAUTH_TOKEN


class Api_Client:
    def __init__(self) -> None:
        self.TOKEN = OAUTH_TOKEN
        self.session = requests.Session()
        if self.TOKEN:
            self.session.headers.update({"Authorization": f"OAuth {self.TOKEN}"})

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get(self, url, params=None, data=None):
        return self.session.get(url, params=params, data=data)

    def post(self, url, params=None, data=None, files=None):
        return self.session.post(url, params=params, data=data, files=files)

    def put(self, url, params=None, data=None, files=None):
        return self.session.put(url, params=params, data=data, files=files)

    def delete(self, url, params=None, data=None, files=None):
        return self.session.delete(url, params=params, data=data, files=files)
