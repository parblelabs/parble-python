from unittest.mock import ANY, patch

import pytest

from parble import ParbleAPIClient


def test_create_client(url, api_key):
    cl = ParbleAPIClient(url, api_key)

    assert cl.settings.url == url
    assert cl.settings.api_key.get_secret_value() == api_key


@pytest.mark.parametrize(
    "method,kwargs",
    (
        ("get", dict(allow_redirects=True)),
        ("post", dict(data=None, json=None)),
        ("patch", dict(data=None)),
        ("delete", {}),
    ),
)
def test_timeout_set_default(api_client, method, kwargs):
    with patch("parble.session.BaseSession.request") as m:
        req = getattr(api_client, method)
        req("files/foobar")
        m.assert_called_once_with(method.upper(), "files/foobar", **kwargs)


@pytest.mark.parametrize(
    "method,kwargs",
    (
        ("get", dict(allow_redirects=True)),
        ("post", dict(data=None, json=None)),
        ("patch", dict(data=None)),
        ("delete", {}),
    ),
)
def test_timeout_override_default(api_client, method, kwargs):
    with patch("parble.session.BaseSession.request") as m:
        req = getattr(api_client, method)
        req("files/foobar", timeout=42)
        m.assert_called_once_with(method.upper(), "files/foobar", timeout=42, **kwargs)

        assert 42 != api_client.settings.default_timeout
