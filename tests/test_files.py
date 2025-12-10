from models.models import FileError, FileResponse
from utils.assertion_helper import assert_error_response as a_error
from utils.assertion_helper import assert_success_response as a_succes


def test_upload_n_copy(folder_manager, create_test_file, file_methods):
    folder_manager("upload")
    file = create_test_file["filename"]
    fim = file_methods

    resp_href = fim.get_link_to_upload("input_data", file)
    assert resp_href.status_code == 200
    a_succes(resp_href, FileResponse)
    href = resp_href.json()["href"]

    resp_upload = fim.upload_file(href, file)
    assert resp_upload.status_code == 201

    resp_copy = fim.copy_file("input_data", "output_data", file)
    assert resp_copy.status_code == 201
    a_succes(resp_copy, FileResponse)

    resp_copy_fail = fim.copy_file("input_data", "output_data", file)
    assert resp_copy_fail.status_code == 409
    a_error(resp_copy_fail, FileError)


def test_download_file(pre_upload_file, file_methods):
    file = pre_upload_file["filename"]
    data = pre_upload_file["data"]
    fim = file_methods
    resp_href = fim.get_link_to_download("sdet_data2", file)
    assert resp_href.status_code == 200
    a_succes(resp_href, FileResponse)
    href = resp_href.json()["href"]
    resp = fim.download_file(href)
    assert resp.status_code == 200
    expected = data.replace("\r\n", "\n").strip()
    actual = resp.text.replace("\r\n", "\n").strip()
    assert actual == expected
