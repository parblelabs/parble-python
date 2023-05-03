from unittest.mock import patch

from parble.models import File


def test_file_create_not_done(sdk, dummy_file_attributes):
    dummy_file_attributes["timings"]["done"] = None
    file = File(sdk=sdk, **dummy_file_attributes)
    assert file.id == dummy_file_attributes["id"]
    assert file.timings.done is None


def test_file_create(sdk, dummy_file_attributes):
    file = File(sdk=sdk, **dummy_file_attributes)
    assert file.id == dummy_file_attributes["id"]


def test_file_pdf(dummy_file):
    with patch("parble.sdk.ParbleSDK.Files.get_pdf") as m:
        pdf = dummy_file.pdf
        m.assert_called_once_with(dummy_file.id)
        assert pdf == m.return_value


def test_file_name(dummy_file):
    assert dummy_file.name == dummy_file.filename


def test_file_iter(dummy_file):
    assert list(dummy_file) == dummy_file.documents


def test_file_get_item(dummy_file):
    assert dummy_file[0] == dummy_file.documents[0]
