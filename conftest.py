import pytest

from utils.api_client import APIClient


@pytest.fixture
def client():
    with APIClient() as api_client:
        yield api_client


@pytest.fixture
def unauthorized_client():
    with APIClient() as api_client:
        api_client.session.headers.pop("Authorization", None)
        yield api_client
