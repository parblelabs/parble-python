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


def test_to_json(dummy_file):
    json_data = dummy_file.to_json()

    assert (
        json_data
        == '{"id": "631bafa2b9753d4ce1e210d0", "timings": {"upload": "2022-11-19 09:42:51", "done": "2022-11-19 09:42:59"}, "filename": "Example.pdf", "automated": false, "number_of_pages": 1, "documents": [{"automated": false, "classification": {"automated": true, "document_type": "invoice", "confidence": 94.0, "start_page": 0, "end_page": 1}, "header_fields": {}, "tables": {}}]}'
    )


def test_from_json(dummy_file):
    json_data = '{"id": "631bafa2b9753d4ce1e210d0", "timings": {"upload": "2022-11-19 09:42:51", "done": "2022-11-19 09:42:59"}, "filename": "Example.pdf", "automated": false, "number_of_pages": 1, "documents": [{"automated": false, "classification": {"automated": true, "document_type": "invoice", "confidence": 94.0, "start_page": 0, "end_page": 1}, "header_fields": {}, "tables": {}}]}'
    file = File.from_json(json_data)

    assert file == dummy_file


def test_json_from_file(dummy_file, dummy_file_attributes):
    import json

    a = json.dumps(dummy_file_attributes)
    assert a == dummy_file.to_json()
