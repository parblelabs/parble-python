import pytest

from parble import ParbleAPIClient, ParbleSDK, Settings


@pytest.fixture
def url():
    return "https://api.parble.com/v1/"


@pytest.fixture
def api_key():
    return "FooBar"


@pytest.fixture
def settings(url, api_key):
    return Settings(url=url, api_key=api_key)


@pytest.fixture
def api_client(url, api_key):
    return ParbleAPIClient(url, api_key)


@pytest.fixture
def sdk(url, api_key):
    return ParbleSDK(url, api_key)


@pytest.fixture
def text():
    return """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Donec elementum in turpis et interdum.
        Praesent a dolor condimentum nisi pretium sodales sollicitudin eu augue.
        Proin consequat tempus felis, vitae malesuada metus vulputate a."""
