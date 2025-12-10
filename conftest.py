import os

import allure
import pytest

from utils.api_client import Api_Client
from utils.api_methods import FilesMethods, FolderMethods


@pytest.fixture
def client(scope="session"):
    with Api_Client() as api_client:
        yield api_client


@pytest.fixture(scope="session")
def create_test_file():
    filename = "data.txt"

    def _clean():
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except OSError as e:
                print(f"Warning: Could not remove file {filename}: {e}")

    try:
        with open(filename, "w") as f:
            data = "username=SDET\npassword=secret_key\n"
            f.write(data)

        yield {"filename": filename, "data": data}

    finally:
        _clean()


@pytest.fixture
def file_methods(client):
    return FilesMethods(client)


@pytest.fixture
def folder_methods(client):
    return FolderMethods(client)


@pytest.fixture(scope="session")
def folder_manager(client, folder_methods):
    folders = []
    fom = folder_methods

    @allure.step("Создать тестовые папки")
    def create_folder(case):
        if case not in ["upload", "download"]:
            raise ValueError("There is no such testcase")
        if case == "download":
            fom.create_folder("sdet_data2")
            folders.append("sdet_data2")
        elif case == "upload":
            fom.create_folder("input_data")
            folders.append("input_data")
            fom.create_folder("output_data")
            folders.append("output_data")

    yield create_folder

    try:
        for f in folders:
            try:
                fom.delete_folder(f)
            except Exception as e:
                print(f"Could not delete folder {f}: {e}")
        fom.clear_trash()
    except Exception as e:
        print(f"Could not clear trash: {e}")


@pytest.fixture
def pre_upload_file(file_methods, create_test_file, folder_manager):
    folder_manager("download")
    f = create_test_file["filename"]
    data = create_test_file["data"]
    fim = file_methods
    resp = fim.get_link_to_upload("sdet_data2", f)
    href = resp.json()["href"]
    fim.upload_file(href, f)
    yield {"filename": f, "data": data}
