import allure

from configs.config import RESOURCE_ENDPOINT, TRASH_ENDPOINT


class FolderMethods:
    def __init__(self, client):
        self.folder_endpoint = RESOURCE_ENDPOINT
        self.trash_endpoint = TRASH_ENDPOINT
        self.api_client = client

    @allure.step("Создать папку")
    def create_folder(self, path):
        params = {"path": f"/{path}"}
        return self.api_client.put(self.folder_endpoint, params=params)

    @allure.step("Удалить папку")
    def delete_folder(self, path):
        params = {"path": f"/{path}"}
        return self.api_client.delete(self.folder_endpoint, params=params)

    @allure.step("Очистить коризну")
    def clear_trash(self):
        self.api_client.delete(self.trash_endpoint)


class FilesMethods:
    def __init__(self, client) -> None:
        self.api_client = client
        self.file_endpoint = RESOURCE_ENDPOINT

    @allure.step("Получить ссылку для загрузки файла")
    def get_link_to_upload(self, folder, file):
        get_link_endp = f"{self.file_endpoint}upload"
        params = {"path": f"/{folder}/{file}"}
        return self.api_client.get(get_link_endp, params=params)

    @allure.step("Загрузить файл")
    def upload_file(self, href, file):
        href = href
        with open(file, "rb") as f:
            files = {"file": (file, f)}
            resp = self.api_client.put(href, files=files)
        return resp

    @allure.step("Скопировать файл в папку output_data")
    def copy_file(self, infolder, outfolder, file):
        url = f"{self.file_endpoint}copy"
        params = {"from": f"/{infolder}/{file}", "path": f"/{outfolder}/{file}"}
        return self.api_client.post(url, params=params)

    @allure.step("Получить ссылку для скачивания файла")
    def get_link_to_download(self, folder, file):
        get_link_endp = f"{self.file_endpoint}download"
        params = {"path": f"/{folder}/{file}"}
        return self.api_client.get(get_link_endp, params=params)

    @allure.step("Скачать файл")
    def download_file(self, href):
        response = self.api_client.get(href)
        return response
