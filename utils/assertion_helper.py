from utils.validator import response_validation


def assert_success_response(data, model, schema):
    val_data = response_validation(data, model, schema)
    assert val_data.method is not None, "Missing 'method' field"
    assert val_data.href is not None, "Missing 'href' field"
    assert val_data.templated is not None, "Missing 'templated' field"
    return val_data


def assert_error_response(data, model, schema):
    val_data = response_validation(data, model, schema)
    assert val_data.error is not None, "Missing 'error' field"
    assert val_data.description is not None, "Missing 'description' field"
    assert val_data.message is not None, "Missing 'message' field"
    return val_data
