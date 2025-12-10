import os
import time

import allure
import pytest

from utils.api_client import Api_Client
from utils.api_methods import FilesMethods, FolderMethods


@pytest.fixture(scope="session")
def client():
    with Api_Client() as api_client:
        yield api_client


@pytest.fixture(scope="session")
def create_test_file():
    filenames = []

    @allure.step("Создать тестовый файл")
    def test_file(filename="data.txt"):
        try:
            with open(filename, "w") as f:
                data = "username=SDET\npassword=secret_key\n"
                f.write(data)
                filenames.append(filename)
            return {"filename": filename, "data": data}
        except OSError as e:
            print(f"Warning: Could not create file {filename}: {e}")

    yield test_file

    for f in filenames:
        if os.path.exists(f):
            try:
                os.remove(f)
            except OSError as e:
                print(f"Warning: Could not remove file {f}: {e}")


@pytest.fixture(scope="session")
def file_methods(client):
    return FilesMethods(client)


@pytest.fixture(scope="session")
def folder_methods(client):
    return FolderMethods(client)


@pytest.fixture(scope="session")
def folder_manager(folder_methods):
    folders = []
    fom = folder_methods

    @allure.step("Создать тестовые папки")
    def create_folder(case):
        if case not in ["upload", "download", "files_list"]:
            raise ValueError("There is no such testcase")
        if case == "download":
            fom.create_folder("sdet_data")
            folders.append("sdet_data")
        elif case == "upload":
            fom.create_folder("input_data")
            folders.append("input_data")
            fom.create_folder("output_data")
            folders.append("output_data")
        elif case == "files_list":
            fom.create_folder("TestFolder")
            folders.append("TestFolder")

    yield create_folder

    try:
        for f in folders:
            try:
                fom.delete_folder(f)
            except Exception as e:
                print(f"Could not delete folder {f}: {e}")
        time.sleep(2)
        fom.clear_trash()
    except Exception as e:
        print(f"Could not clear trash: {e}")


@pytest.fixture
def pre_upload_file(file_methods, create_test_file):
    @allure.step("Создать тестовые файлы в папке")
    def pre_test_entities(folder, filenames=["data.txt"]):
        if isinstance(filenames, str):
            filenames = [filenames]

        uploaded_files = []

        for filename in filenames:
            f = create_test_file(filename)
            data = f["data"]
            fim = file_methods
            resp = fim.get_link_to_upload(folder, filename)
            href = resp.json()["href"]
            fim.upload_file(href, filename)
            uploaded_files.append({"filename": filename, "data": data})

        return uploaded_files

    yield pre_test_entities
