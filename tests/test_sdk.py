from io import BytesIO
from unittest.mock import ANY, patch

from parble import ParbleSDK
from parble.models import File


def test_create(url, api_key):
    sdk = ParbleSDK(url, api_key)

    assert sdk.client.settings.url == url


def test_upload_path(sdk, tmp_path, text, dummy_file_attributes):
    """ This tests the SDK's Files post method, which uploads a file from a specified path"""
    name = "test_upload.txt"
    path = tmp_path / name
    with open(path, "w") as f:
        f.write(text)

    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dummy_file_attributes
        rv = sdk.files.post(str(path))
        assert isinstance(rv, File)
        assert rv.id == dummy_file_attributes["id"]
        m.assert_called_once_with(ANY, name, content_type="text/plain", inbox_id=None)
        f = m.call_args[0][0]
        assert f.name == str(path)

def test_upload_path_custom_inbox(sdk, tmp_path, text, dummy_file_attributes):
    """ This tests the SDK's Files post method with a custom inbox id"""
    name = "test_upload.txt"
    path = tmp_path / name
    with open(path, "w") as f:
        f.write(text)

    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dummy_file_attributes
        rv = sdk.files.post(str(path), inbox_id="636baf52b9753d4ce1e210d0")
        assert isinstance(rv, File)
        assert rv.id == dummy_file_attributes["id"]
        m.assert_called_once_with(ANY, name, content_type="text/plain", inbox_id="636baf52b9753d4ce1e210d0")
        f = m.call_args[0][0]
        assert f.name == str(path)

def test_upload_file_default(sdk, text, dummy_file_attributes):
    """ This tests the SDK's Files post file method with default options"""
    buf = BytesIO(text.encode())
    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dummy_file_attributes
        rv = sdk.files.post_file(buf, "foo.txt")
        assert rv.id == dummy_file_attributes["id"]
        m.assert_called_once_with(buf, "foo.txt", content_type="application/octet-stream", inbox_id=None)


def test_upload_file_override_content_type(sdk, text, dummy_file_attributes):
    buf = BytesIO(text.encode())
    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dummy_file_attributes
        rv = sdk.files.post_file(buf, "foo.txt", "text/plain")
        assert rv.id == dummy_file_attributes["id"]
        m.assert_called_once_with(buf, "foo.txt", content_type="text/plain", inbox_id=None)

def test_upload_file_custom_inbox(sdk, text, dummy_file_attributes):
    buf = BytesIO(text.encode())
    with patch("parble.resources.files.FilesResource.post") as m:
        m.return_value = dummy_file_attributes
        rv = sdk.files.post_file(buf, "foo.txt", "text/plain", "636baf52b9753d4ce1e210d0")
        assert rv.id == dummy_file_attributes["id"]
        m.assert_called_once_with(buf, "foo.txt", content_type="text/plain", inbox_id="636baf52b9753d4ce1e210d0")



def test_get_file(sdk, dummy_file_attributes):
    pk = "636baf52b9753d4ce1e210d0"
    with patch("parble.resources.files.FilesResource.get") as m:
        m.return_value = dummy_file_attributes
        rv = sdk.files.get(pk)
        assert isinstance(rv, File)
        assert rv.id == dummy_file_attributes["id"]


def test_get_file_pdf(sdk):
    pk = "636baf52b9753d4ce1e210d0"
    b = b"%PDF-1.3\n3 0 %%EOF\n"
    with patch("parble.resources.files.FilesResource.get") as m:
        m.return_value = b
        rv = sdk.files.get_pdf(pk)
        assert isinstance(rv, BytesIO)
        assert rv.read() == b


def test_create_file(sdk, dummy_file_attributes):
    f = sdk.files.create(**dummy_file_attributes)

    assert f.id == dummy_file_attributes["id"]
    assert f._sdk == sdk
