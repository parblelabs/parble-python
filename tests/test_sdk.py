from io import BytesIO
from unittest.mock import ANY, patch

from parble import ParbleSDK
from parble.models import File


def test_create(url, api_key):
    sdk = ParbleSDK(url, api_key)

    assert sdk.client.settings.url == url


def test_upload_path(sdk, tmp_path, text):
    name = "test_upload.txt"
    path = tmp_path / name
    pk = "636baf52b9753d4ce1e210d0"
    with open(path, "w") as f:
        f.write(text)

    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dict(id=pk)
        rv = sdk.upload_path(str(path))
        assert isinstance(rv, File)
        assert rv.id == pk
        m.assert_called_once_with(ANY, name, content_type="text/plain")
        f = m.call_args[0][0]
        assert f.name == str(path)


def test_upload_file_default_content_type(sdk, text):
    buf = BytesIO(text.encode())
    pk = "636baf52b9753d4ce1e210d0"
    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dict(id=pk)
        rv = sdk.upload_file(buf, "foo.txt")
        assert rv.id == pk
        m.assert_called_once_with(buf, "foo.txt", content_type="application/octet-stream")


def test_upload_file_override_content_type(sdk, text):
    buf = BytesIO(text.encode())
    pk = "636baf52b9753d4ce1e210d0"
    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dict(id=pk)
        rv = sdk.upload_file(buf, "foo.txt", "text/plain")
        assert rv.id == pk
        m.assert_called_once_with(buf, "foo.txt", content_type="text/plain")


def test_get_file(sdk):
    pk = "636baf52b9753d4ce1e210d0"
    with patch("parble.resources.files.FilesResource.get") as m:
        m.return_value = dict(id=pk)
        rv = sdk.get_file(pk)
        assert isinstance(rv, File)
        assert rv.id == pk


def test_get_file_pdf(sdk):
    pk = "636baf52b9753d4ce1e210d0"
    b = b"%PDF-1.3\n3 0 %%EOF\n"
    with patch("parble.resources.files.FilesResource.get") as m:
        m.return_value = b
        rv = sdk.get_file_pdf(pk)
        assert isinstance(rv, BytesIO)
        assert rv.read() == b


def test_create_file(sdk):
    pk = "636baf52b9753d4ce1e210d0"
    attrs = dict(id=pk)
    f = sdk.create_file(attrs)

    assert f.id == pk
    assert f._sdk == sdk
