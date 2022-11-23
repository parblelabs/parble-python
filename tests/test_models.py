from unittest.mock import patch

from parble.models import File


def test_file_create(sdk):
    pk = "631bafa2b9753d4ce1e210d0"
    file = File(id=pk, sdk=sdk)
    assert file.id == pk


def test_file_pdf(sdk):
    pk = "631bafa2b975ac4ce1e210d0"
    file = File(id=pk, sdk=sdk)
    with patch("parble.sdk.ParbleSDK.get_file_pdf") as m:
        pdf = file.pdf
        m.assert_called_once_with(pk)
        assert pdf == m.return_value
