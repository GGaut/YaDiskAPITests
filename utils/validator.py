import allure
from jsonschema import validate


@allure.step("Валидация/сериализация")
def response_validation(response, model_class, schema):
    data = response.json()
    validate(instance=data, schema=schema)
    return model_class.from_dict(data)
