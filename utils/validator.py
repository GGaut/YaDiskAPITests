from typing import Any, Type, TypeVar

import allure
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@allure.step("Валидация/сериализация данных ответа")
def response_validation(data, model: Type[T]) -> dict[str, Any]:
    try:
        json_data = data.json()
        v_data = model.model_validate(json_data)
        return v_data.model_dump()
    except Exception as e:
        raise ValueError(f"Validation error: {e}")
