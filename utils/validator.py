from typing import Any, Type, TypeVar

import allure
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@allure.step("Валидация/сериализация данных ответа")
def response_validation(data: dict[str, Any], model: Type[T]) -> T:
    try:
        v_data = model.model_validate(data)
        v_data.model_dump()
        return v_data
    except Exception as e:
        raise ValueError(f"Validation error: {e}")
