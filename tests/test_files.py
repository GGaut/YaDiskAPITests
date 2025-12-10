import allure

from models.models import FileError, FileResponse, FilesResponse
from utils.assertion_helper import assert_error_response as a_error
from utils.assertion_helper import assert_success_response as a_succes
from utils.validator import response_validation


@allure.feature("Операции с файлами")
@allure.title("Загрузить файл на ядиск и скопировать его в другую папку")
def test_upload_n_copy(folder_manager, create_test_file, file_methods):
    folder_manager("upload")
    create_file = create_test_file()
    file = create_file["filename"]
    fim = file_methods

    resp_href = fim.get_link_to_upload("input_data", file)
    assert resp_href.status_code == 200, (
        f"Request returns {resp_href.status_code} code, expected 200"
    )
    href = a_succes(resp_href, FileResponse)["href"]

    resp_upload = fim.upload_file(href, file)
    assert resp_upload.status_code == 201, (
        f"Request returns {resp_upload.status_code} code, expected 201"
    )

    resp_copy = fim.copy_file("input_data", "output_data", file)
    assert resp_copy.status_code == 201, (
        f"Request returns {resp_copy.status_code} code, expected 201"
    )
    a_succes(resp_copy, FileResponse)

    resp_copy_fail = fim.copy_file("input_data", "output_data", file)
    assert resp_copy_fail.status_code == 409, (
        f"Request returns {resp_copy_fail.status_code} code, expected 409"
    )
    a_error(resp_copy_fail, FileError)


@allure.feature("Операции с файлами")
@allure.title("Скачать загруженный файл")
def test_download_file(pre_upload_file, file_methods, folder_manager):
    folder_manager("download")
    folder, filename = "sdet_data", "data.txt"
    create_file = pre_upload_file(folder, filename)
    data = create_file[0]["data"]
    fim = file_methods
    resp_href = fim.get_link_to_download("sdet_data", filename)
    assert resp_href.status_code == 200, (
        f"Request returns {resp_href.status_code} code, expected 200"
    )
    href = a_succes(resp_href, FileResponse)["href"]
    resp = fim.download_file(href)
    assert resp.status_code == 200, (
        f"Request returns {resp.status_code} code, expected 200"
    )
    expected = data.replace("\r\n", "\n").strip()
    actual = resp.text.replace("\r\n", "\n").strip()
    assert actual == expected


@allure.feature("Операции с файлами")
@allure.title("Получить список файлов на ядиске")
def test_get_file_list(pre_upload_file, file_methods, folder_manager):
    folder_manager("files_list")
    folder, f1, f2 = "TestFolder", "data1.txt", "data2.txt"
    pre_upload_file(folder, [f1, f2])
    fim = file_methods
    resp = fim.get_files_list(folder)
    assert resp.status_code == 200, (
        f"Request returns {resp.status_code} code, expected 200"
    )
    resp = response_validation(resp, FilesResponse)
    files = [
        {"name": item["name"]}
        for item in resp["items"]
        if f"/{folder}/" in item["path"]
    ]
    assert {"name": f1} in files, f"Missing value {f1} in name filed"
    assert {"name": f2} in files, f"Missing value {f2} in name filed"
