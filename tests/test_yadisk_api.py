import allure

from models.models import DI_ErrorResponse, DiskInfoResponse
from utils.validator import response_validation


@allure.title("Авторизация с валидным токеном")
@allure.step("Отправить GET запрос с авторизацией")
def test_auth_with_valid_token(client):
    response = client.get()

    assert response.status_code == 200, (
        f"Request returns {response.status_code} code, expected 200"
    )
    data = response.json()
    val_data = response_validation(data, DiskInfoResponse)

    # Проверяем, что поля существуют и не None
    assert "user" in val_data and val_data["user"] is not None, (
        "Response body doesn't contain 'user' field"
    )
    assert "login" in val_data["user"] and val_data["user"]["login"] is not None, (
        "Response body doesn't contain 'login' field"
    )
    assert (
        "display_name" in val_data["user"]
        and val_data["user"]["display_name"] is not None
    ), "Response body doesn't contain 'display_name' field"


@allure.title("Авторизация без токена")
@allure.step("Отправить GET запрос без авторизации")
def test_auth_without_token(unauthorized_client):
    response = unauthorized_client.get()

    assert response.status_code == 401, (
        f"Request returns {response.status_code} code, expected 401"
    )
    data = response.json()
    val_data = response_validation(data, DI_ErrorResponse)

    # Проверяем, что поля существуют и не None
    assert "error" in val_data and val_data["error"] is not None, (
        "Error response body doesn't contain 'error' field"
    )
    assert "description" in val_data and val_data["description"] is not None, (
        "Error response body doesn't contain 'description' field"
    )
    assert "message" in val_data and val_data["message"] is not None, (
        "Error response body doesn't contain 'message' field"
    )
