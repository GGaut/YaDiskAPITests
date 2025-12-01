import allure
import requests

from config.configs import API_BASE_URL, OAUTH_TOKEN


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.token = OAUTH_TOKEN
        if self.token:
            self.session.headers.update({"Authorization": f"OAuth {self.token}"})

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @allure.step("Отправить GET запрос")
    def get(self, endpoint=""):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.get(url)

    @allure.step("Отправить POST запрос")
    def post(self, endpoint="", data=None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.post(url, data=data)

    @allure.step("Отправить PUT запрос")
    def put(self, endpoint="", data=None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.put(url, data=data)

    @allure.step("Отправить DELETE запрос")
    def delete(self, endpoint="", data=None):
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        return self.session.delete(url, data=data)
