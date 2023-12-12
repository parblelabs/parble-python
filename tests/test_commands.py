import json
import logging
from io import BytesIO
from unittest.mock import ANY, PropertyMock, patch

import click
import pytest
from click.testing import CliRunner
from parble import ParbleSDK

from parble.commands import NAME, get, parble, upload


@pytest.fixture
def runner():
    return CliRunner(mix_stderr=False)


@pytest.fixture
def config_envvars(monkeypatch, url, api_key):
    monkeypatch.setenv("PARBLE_URL", url)
    monkeypatch.setenv("PARBLE_API_KEY", api_key)


@pytest.fixture
def command_foo():
    @click.command()
    def foo():
        logger = logging.getLogger(NAME)
        logger.error("ERR")
        logger.warning("WARN")
        logger.info("INF")
        logger.debug("DEB")

    parble.add_command(foo)
    yield
    parble.commands.pop("foo")


@pytest.fixture()
def mock_files_post(dummy_file_attributes):
    def files_post(self: ParbleSDK.Files, _, inbox_id):
        """This mocks the post method of the Files class on the ParbleSDK"""
        return self.create(**dummy_file_attributes)

    return files_post


def test_upload(runner, tmp_path, config_envvars, text, mock_files_post, dummy_file_attributes):
    name = "test_upload.txt"
    path = tmp_path / name

    # Writing the test file into a temp path
    with open(path, "w") as f:
        f.write(text)

    with patch("parble.sdk.ParbleSDK.Files.post", autospec=True) as m:
        m.side_effect = mock_files_post
        # We invoke the runner with the temp path of the test file
        res = runner.invoke(upload, [str(path)])
        assert res.exit_code == 0, res.output
        # We verify the (mocked) Files post method was called with this path and empty inbox
        m.assert_called_once_with(ANY, path, inbox_id=None)
        data = json.loads(res.output)
        assert data["id"] == dummy_file_attributes["id"]
        assert data["filename"] == dummy_file_attributes["filename"]
        assert data["automated"] == dummy_file_attributes["automated"]
        assert data["number_of_pages"] == dummy_file_attributes["number_of_pages"]
        assert "timings" in data
        assert "documents" in data
        docs = data["documents"]
        assert len(docs) == 1


def test_upload_custom_inbox(runner, tmp_path, config_envvars, text, mock_files_post, dummy_file_attributes):
    name = "test_upload.txt"
    path = tmp_path / name

    # Writing the test file into a temp path
    with open(path, "w") as f:
        f.write(text)

    with patch("parble.sdk.ParbleSDK.Files.post", autospec=True) as m:
        m.side_effect = mock_files_post
        # We invoke the runner with the temp path of the test file
        res = runner.invoke(upload, [str(path), "-i636baf52b9753d4ce1e210d0"])
        assert res.exit_code == 0, res.output
        # We verify the (mocked) Files post method was called with this path and inbox
        m.assert_called_once_with(ANY, path, inbox_id="636baf52b9753d4ce1e210d0")
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

    with patch("parble.sdk.ParbleSDK.Files.get") as m:
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

    with patch("parble.sdk.ParbleSDK.Files.get") as m, patch("parble.models.File.pdf", new_callable=PropertyMock) as f:
        m.side_effect = _get
        f.return_value = BytesIO(b)
        res = runner.invoke(get, [dummy_file.id, "--format", "pdf"])

        m.assert_called_once_with(dummy_file.id)
        f.assert_called_once()

    assert res.exit_code == 0
    assert res.stdout_bytes == b + b"\n"


def test_missing_envvars(runner):
    with patch("parble.sdk.ParbleSDK.Files.get") as m:
        res = runner.invoke(parble, ["file", "get", "foobar"])
        assert m.call_count == 0
    assert res.stderr
    lines = res.stderr.split("\n")
    assert len(lines) == 3, lines
    assert lines[0] == "error: Parble SDK Configuration Error!"
    assert lines[1] == "error: missing or incorrect settings value for url, api_key"
    assert lines[2] == ""


@pytest.mark.parametrize("verbose", (None, "-v", "-vv", "-vvv"))
def test_verbose(runner, verbose, command_foo):
    args = [verbose, "foo"] if verbose else ["foo"]
    v = verbose.count("v") if verbose else 0

    res = runner.invoke(parble, args)

    levels = ["error", "warning", "info", "debug", "debug"]
    level = levels[v]
    hidden_levels = levels[v + 1 :]
    assert level in res.stderr
    for l in hidden_levels:
        if l == level:
            continue
        assert l not in res.stderr
