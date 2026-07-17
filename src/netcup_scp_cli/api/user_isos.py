"""User ISOs (S3) API - list, delete, download URL, upload."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .base import get_client
from .s3_upload import DEFAULT_PART_SIZE, upload_file


def user_isos_list(user_id: int) -> list[dict]:
    """GET /api/v1/users/{userId}/isos."""
    client = get_client()
    resp = client.get(f"/users/{user_id}/isos")
    return resp.json()


def user_iso_delete(user_id: int, key: str) -> None:
    """DELETE /api/v1/users/{userId}/isos/{key}."""
    client = get_client()
    client.delete(f"/users/{user_id}/isos/{key}")


def user_iso_download_url(user_id: int, key: str) -> str | dict:
    """GET /api/v1/users/{userId}/isos/{key} - Get presigned download URL."""
    client = get_client()
    resp = client.get(f"/users/{user_id}/isos/{key}")
    data = resp.json()
    if isinstance(data, str):
        return data
    return data.get("presignedUrl", data) if isinstance(data, dict) else data


def user_iso_prepare_upload(user_id: int, key: str, *, multipart: bool = True) -> dict:
    """POST /api/v1/users/{userId}/isos/{key}?multipart=..."""
    client = get_client()
    resp = client.post(
        f"/users/{user_id}/isos/{key}",
        params={"multipart": str(multipart).lower()},
    )
    return resp.json()


def user_iso_sign_part(user_id: int, key: str, upload_id: str, part_number: int) -> str:
    """GET /api/v1/users/{userId}/isos/{key}/{uploadId}/parts/{partNumber}."""
    client = get_client()
    resp = client.get(f"/users/{user_id}/isos/{key}/{upload_id}/parts/{part_number}")
    data = resp.json()
    if isinstance(data, dict) and "url" in data:
        return data["url"]
    raise ValueError(f"Unexpected sign-part response: {data!r}")


def user_iso_complete_upload(
    user_id: int,
    key: str,
    upload_id: str,
    parts: list[dict[str, Any]],
) -> None:
    """PUT /api/v1/users/{userId}/isos/{key}/{uploadId} with S3CompletedPart[]."""
    client = get_client()
    client.put(f"/users/{user_id}/isos/{key}/{upload_id}", json=parts)


def user_iso_upload(
    user_id: int,
    key: str,
    file_path: Path | str,
    *,
    part_size: int = DEFAULT_PART_SIZE,
    use_multipart: bool | None = None,
    on_progress: Callable[[int, int], None] | None = None,
) -> None:
    """Upload a local file as a user ISO (single-shot or S3 multipart)."""
    upload_file(
        Path(file_path),
        prepare=lambda multipart: user_iso_prepare_upload(user_id, key, multipart=multipart),
        sign_part=lambda upload_id, part_number: user_iso_sign_part(
            user_id, key, upload_id, part_number
        ),
        complete=lambda upload_id, parts: user_iso_complete_upload(user_id, key, upload_id, parts),
        part_size=part_size,
        use_multipart=use_multipart,
        on_progress=on_progress,
    )
