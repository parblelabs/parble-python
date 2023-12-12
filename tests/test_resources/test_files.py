from io import BytesIO

import pytest
import requests

from parble import exceptions
from parble.resources.files import FilesResource


@pytest.fixture
def files_resource(api_client):
    return FilesResource(api_client)


def test_delete(files_resource, requests_mock, url):
    pk = "636baf52b9753d4ce1e210d0"

    requests_mock.delete(f"{url}files/{pk}", status_code=204)
    rv = files_resource.delete(pk)
    assert rv is None


def test_get(files_resource, requests_mock, url):
    pk = "636baf52b9753d4ce1e210d0"
    requests_mock.get(
        f"{url}files/{pk}",
        json=dict(id=pk),
        headers={"Content-Type": "application/json"},
    )
    rv = files_resource.get(pk)

    assert rv == dict(id=pk)


def test_get_not_found(files_resource, requests_mock, url):
    pk = "636baf52b9753d4ce1e210d0"
    requests_mock.get(f"{url}files/{pk}", status_code=404)
    with pytest.raises(exceptions.NotFoundError):
        files_resource.get(pk)


def test_post(files_resource, requests_mock, url, text):
    pk = "636baf52b9753d4ce1e210d0"
    buf = BytesIO(text.encode())

    requests_mock.post(f"{url}files", json=dict(id=pk))

    rv = files_resource.post(buf, "lorem.txt", content_type="text/plain")

    assert rv == dict(id=pk)

def test_post_custom_inbox(files_resource, requests_mock, url, text):
    pk = "636baf52b9753d4ce1e210d0"
    inbox_id = "636baf52b9753d4ce1e210d0"
    buf = BytesIO(text.encode())

    requests_mock.post(f"{url}files", json=dict(id=pk))

    rv = files_resource.post(buf, "lorem.txt", inbox_id=inbox_id, content_type="text/plain")

    assert rv == dict(id=pk)


def test_post_timed_out(files_resource, requests_mock, url, text):
    buf = BytesIO(text.encode())
    requests_mock.post(f"{url}files", exc=requests.exceptions.Timeout)

    with pytest.raises(exceptions.CallTimeoutError):
        files_resource.post(buf, "lorem.txt", content_type="text/plain")


def test_post_see_other(files_resource, requests_mock, url, text):
    """
    If the sync processing timed-out, it's returning a 303 redirect to the file
    """
    pk = "636baf52b9753d4ce1e217d8"
    buf = BytesIO(text.encode())
    requests_mock.post(f"{url}files", status_code=303, headers={"Location": f"{url}files/{pk}"})
    requests_mock.get(f"{url}files/{pk}", json=dict(id=pk))

    rv = files_resource.post(buf, "lorem.txt", content_type="text/plain")
    assert rv == dict(id=pk)
