import pytest
from requests import Request, exceptions

from parble import __version__
from parble.exceptions import APICallError
from parble.session import BaseSession


@pytest.fixture
def session(settings):
    return BaseSession(settings)


def test_initialize(settings):
    sess = BaseSession(settings)

    assert sess.headers["X-API-Key"] == settings.api_key.get_secret_value()
    assert sess.headers["Accept"] == "application/json"
    assert sess.headers["User-Agent"] == f"parble-python/{__version__}"


@pytest.mark.parametrize(
    "uri, full_url",
    (
        ("files/abcdef", "https://api.parble.com/v1/files/abcdef"),
        ("/foo", "https://api.parble.com/foo"),
    ),
)
def test_build_url(settings, session, uri, full_url):
    assert session.build_url(uri) == full_url


@pytest.mark.parametrize("method", ("GET", "DELETE", "PATCH", "POST"))
def test_request(session, method, requests_mock):
    m = requests_mock.register_uri(method, "https://api.parble.com/v1/files/foobar")
    session.request(method, "files/foobar")

    assert m.called_once
    req = m.last_request
    assert req.timeout == session._settings.default_timeout


@pytest.mark.parametrize("method", ("GET", "DELETE", "PATCH", "POST"))
def test_prepare_request(session, method, requests_mock):
    req = Request(method, "files/foobar")
    session.prepare_request(req)
    assert req.url == "https://api.parble.com/v1/files/foobar"


@pytest.mark.parametrize("method", ("GET", "DELETE", "PATCH", "POST"))
def test_request_override_timeout(session, method, requests_mock):
    m = requests_mock.register_uri(method, "https://api.parble.com/v1/files/foobar")
    session.request(method, "files/foobar", timeout=42)

    assert m.called_once
    req = m.last_request
    assert req.timeout == 42


@pytest.mark.parametrize(
    "exc", (exceptions.SSLError, exceptions.Timeout, exceptions.ConnectionError, exceptions.RequestException)
)
def test_request_raises_api_call_error(session, requests_mock, exc):
    m = requests_mock.register_uri("GET", "https://api.parble.com/v1/files/foobar", exc=exc("Boom"))
    with pytest.raises(APICallError):
        session.request("GET", "files/foobar")

    assert m.called_once
