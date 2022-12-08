import json
from io import BytesIO
from unittest.mock import ANY, PropertyMock, patch

import pytest
from click.testing import CliRunner

from parble.commands import get, upload


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def config_envvars(monkeypatch, url, api_key):
    monkeypatch.setenv("PARBLE_URL", url)
    monkeypatch.setenv("PARBLE_API_KEY", api_key)


def test_upload(runner, tmp_path, config_envvars, text, dummy_file_attributes):
    name = "test_upload.txt"
    path = tmp_path / name

    def upload_path(self, _):
        return self.create_file(**dummy_file_attributes)

    with open(path, "w") as f:
        f.write(text)
    with patch("parble.sdk.ParbleSDK.upload_path", autospec=True) as m:
        m.side_effect = upload_path
        res = runner.invoke(upload, [str(path)])
        assert res.exit_code == 0, res.output
        m.assert_called_once_with(ANY, path)
        data = json.loads(res.output)
        assert data["id"] == dummy_file_attributes["id"]
        assert data["filename"] == dummy_file_attributes["filename"]
        assert data["automated"] == dummy_file_attributes["automated"]
        assert data["number_of_pages"] == dummy_file_attributes["number_of_pages"]
        assert "timings" in data
        assert "documents" in data
        docs = data["documents"]
        assert len(docs) == 1


def test_upload_file_does_not_exist(runner, tmp_path, config_envvars, text):
    name = "does_not_exist.pdf"

    path = tmp_path / name

    res = runner.invoke(upload, [str(path)])

    assert res.exit_code == 2

    assert f"Error: Invalid value for 'FILE': File '{path}' does not exist."


def test_get_file(runner, config_envvars, dummy_file):
    def _get(_):
        return dummy_file

    with patch("parble.sdk.ParbleSDK.get_file") as m:
        m.side_effect = _get

        res = runner.invoke(get, [dummy_file.id])

        m.assert_called_once_with(dummy_file.id)

    assert res.exit_code == 0
    data = json.loads(res.output)

    assert data["id"] == dummy_file.id
    assert data["filename"] == dummy_file.filename
    assert data["automated"] == dummy_file.automated
    assert data["number_of_pages"] == dummy_file.number_of_pages
    assert "timings" in data
    assert "documents" in data
    docs = data["documents"]
    assert len(docs) == 1


def test_get_file_pdf(runner, config_envvars, dummy_file):

    b = b"%PDF-1.3\n3 0 %%EOF\n"

    def _get(_):
        return dummy_file

    with patch("parble.sdk.ParbleSDK.get_file") as m, patch("parble.models.File.pdf", new_callable=PropertyMock) as f:

        m.side_effect = _get
        f.return_value = BytesIO(b)
        res = runner.invoke(get, [dummy_file.id, "--format", "pdf"])

        m.assert_called_once_with(dummy_file.id)
        f.assert_called_once()

    assert res.exit_code == 0
    assert res.stdout_bytes == b + b"\n"
