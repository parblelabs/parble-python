import pytest

from parble import ParbleAPIClient, ParbleSDK, Settings
from parble.models import File


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


@pytest.fixture
def dummy_file_attributes():
    return dict(
        id="631bafa2b9753d4ce1e210d0",
        timings=dict(upload="2022-11-19 09:42:51", done="2022-11-19 09:42:59"),
        filename="Example.pdf",
        automated=False,
        number_of_pages=1,
        documents=[
            dict(
                automated=False,
                classification=dict(
                    automated=True,
                    document_type="invoice",
                    confidence=94.0,
                    start_page=0,
                    end_page=1,
                ),
                header_fields={},
                tables={},
            )
        ],
    )


@pytest.fixture
def dummy_file(sdk, dummy_file_attributes):
    return File(sdk=sdk, **dummy_file_attributes)
