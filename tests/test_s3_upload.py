"""Unit tests for S3 multipart / single-shot upload helpers."""

from pathlib import Path
from unittest.mock import patch

import pytest
import responses

from netcup_scp_cli.api import base as api_base
from netcup_scp_cli.api.s3_upload import put_to_presigned_url, upload_file
from netcup_scp_cli.api.user_images import user_image_upload
from netcup_scp_cli.config import API_BASE_URL
from netcup_scp_cli.exceptions import APIError


@pytest.fixture(autouse=True)
def _reset_client():
    api_base._default_client = None
    yield
    api_base._default_client = None


@responses.activate
def test_put_to_presigned_url_returns_etag() -> None:
    responses.add(
        responses.PUT,
        "https://s3.example/part",
        status=200,
        headers={"ETag": '"abc123"'},
    )
    assert put_to_presigned_url("https://s3.example/part", b"data") == '"abc123"'


@responses.activate
def test_put_to_presigned_url_errors() -> None:
    responses.add(responses.PUT, "https://s3.example/part", status=403, body="denied")
    with pytest.raises(APIError) as exc:
        put_to_presigned_url("https://s3.example/part", b"data")
    assert exc.value.status_code == 403


def test_upload_file_single_shot(tmp_path: Path) -> None:
    f = tmp_path / "img.bin"
    f.write_bytes(b"hello-world")
    completed: list = []
    signed: list = []

    def prepare(multipart: bool) -> dict:
        assert multipart is False
        return {"presignedUrl": "https://s3.example/single"}

    def sign_part(upload_id: str, part_number: int) -> str:
        signed.append((upload_id, part_number))
        return "unused"

    def complete(upload_id: str, parts: list) -> None:
        completed.append((upload_id, parts))

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.PUT,
            "https://s3.example/single",
            status=200,
            headers={"ETag": '"e1"'},
        )
        upload_file(
            f,
            prepare=prepare,
            sign_part=sign_part,
            complete=complete,
            use_multipart=False,
        )

    assert signed == []
    assert completed == []


def test_upload_file_multipart(tmp_path: Path) -> None:
    f = tmp_path / "img.bin"
    f.write_bytes(b"abcdefghij")  # 10 bytes, part_size 4 → 3 parts
    completed: list = []

    def prepare(multipart: bool) -> dict:
        assert multipart is True
        return {"uploadId": "up-1"}

    def sign_part(upload_id: str, part_number: int) -> str:
        assert upload_id == "up-1"
        return f"https://s3.example/p{part_number}"

    def complete(upload_id: str, parts: list) -> None:
        completed.append((upload_id, parts))

    with responses.RequestsMock() as rsps:
        for n in (1, 2, 3):
            rsps.add(
                responses.PUT,
                f"https://s3.example/p{n}",
                status=200,
                headers={"ETag": f'"e{n}"'},
            )
        upload_file(
            f,
            prepare=prepare,
            sign_part=sign_part,
            complete=complete,
            part_size=4,
            use_multipart=True,
        )

    assert len(completed) == 1
    upload_id, parts = completed[0]
    assert upload_id == "up-1"
    assert parts == [
        {"ETag": '"e1"', "partNumber": 1},
        {"ETag": '"e2"', "partNumber": 2},
        {"ETag": '"e3"', "partNumber": 3},
    ]


@responses.activate
@patch("netcup_scp_cli.client.get_access_token", return_value="tok")
def test_user_image_upload_multipart_end_to_end(_token, tmp_path: Path) -> None:
    f = tmp_path / "disk.qcow2"
    f.write_bytes(b"12345678")  # 8 bytes, part_size 3 → 3 parts
    user_id = 42
    key = "my-image"

    responses.add(
        responses.POST,
        f"{API_BASE_URL}/users/{user_id}/images/{key}",
        json={"uploadId": "uid-9"},
        status=201,
    )
    for n in (1, 2, 3):
        responses.add(
            responses.GET,
            f"{API_BASE_URL}/users/{user_id}/images/{key}/uid-9/parts/{n}",
            json={"url": f"https://s3.example/part{n}"},
            status=200,
        )
        responses.add(
            responses.PUT,
            f"https://s3.example/part{n}",
            status=200,
            headers={"ETag": f'"etag{n}"'},
        )
    responses.add(
        responses.PUT,
        f"{API_BASE_URL}/users/{user_id}/images/{key}/uid-9",
        status=204,
    )

    user_image_upload(user_id, key, f, part_size=3, use_multipart=True)

    # Last SCP call should be complete with 3 parts
    complete_calls = [
        c
        for c in responses.calls
        if (
            c.request.method == "PUT"
            and "uid-9" in c.request.url
            and "s3.example" not in c.request.url
        )
    ]
    assert len(complete_calls) == 1
    import json

    body = json.loads(complete_calls[0].request.body)
    assert len(body) == 3
    assert body[0]["partNumber"] == 1
