from parble import Settings


def test_settings_via_init(url, api_key):
    s = Settings(url=url, api_key=api_key)

    assert s.url == url
    assert s.api_key.get_secret_value() == api_key
    assert s.default_timeout == 30


def test_settings_via_envvars(monkeypatch, url, api_key):
    monkeypatch.setenv("PARBLE_URL", url)
    monkeypatch.setenv("PARBLE_API_KEY", api_key)

    s = Settings()

    assert s.url == url
    assert s.api_key.get_secret_value() == api_key
    assert s.default_timeout == 30


def test_url_missing_end_slash(monkeypatch, api_key):
    stripped_url = "https://localhost"
    monkeypatch.setenv("PARBLE_URL", stripped_url)
    monkeypatch.setenv("PARBLE_API_KEY", api_key)

    s = Settings()

    assert s.url == "https://localhost/"


def override_default_timeout(url, api_key):

    s = Settings(url=url, api_key=api_key, default_timeout=42)

    assert s.default_timeout == 42
