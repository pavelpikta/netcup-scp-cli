"""S3 multipart / single-shot upload via SCP prepare/sign/complete APIs."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import requests

from ..exceptions import APIError

DEFAULT_PART_SIZE = 8 * 1024 * 1024  # 8 MiB
S3_PUT_TIMEOUT = 600

ProgressCallback = Callable[[int, int], None]  # bytes_done, total_bytes
PrepareFn = Callable[[bool], dict[str, Any]]
SignPartFn = Callable[[str, int], str]
CompleteFn = Callable[[str, list[dict[str, Any]]], None]


def put_to_presigned_url(url: str, data: bytes) -> str:
    """PUT bytes to a presigned S3 URL; return ETag from response headers."""
    resp = requests.put(url, data=data, timeout=S3_PUT_TIMEOUT)
    if not resp.ok:
        raise APIError(
            f"S3 upload error: {resp.status_code}",
            status_code=resp.status_code,
            body=resp.text,
        )
    etag = resp.headers.get("ETag") or resp.headers.get("etag")
    if not etag:
        raise APIError("S3 upload succeeded but response had no ETag header")
    return etag


def upload_file(
    file_path: Path,
    *,
    prepare: PrepareFn,
    sign_part: SignPartFn,
    complete: CompleteFn,
    part_size: int = DEFAULT_PART_SIZE,
    use_multipart: bool | None = None,
    on_progress: ProgressCallback | None = None,
) -> None:
    """Upload a local file via SCP S3 prepare/sign/complete flow.

    When ``use_multipart`` is None, multipart is used if the file is larger than
    ``part_size``; otherwise a single-shot presigned PUT is used.
    """
    if part_size < 1:
        raise ValueError("part_size must be >= 1")
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    total = path.stat().st_size
    multipart = use_multipart if use_multipart is not None else total > part_size

    if not multipart:
        info = prepare(False)
        url = info.get("presignedUrl")
        if not url:
            raise APIError("Prepare upload did not return presignedUrl for single-shot upload")
        data = path.read_bytes()
        put_to_presigned_url(url, data)
        if on_progress:
            on_progress(total, total)
        return

    info = prepare(True)
    upload_id = info.get("uploadId")
    if not upload_id:
        raise APIError("Prepare upload did not return uploadId for multipart upload")

    completed: list[dict[str, Any]] = []
    bytes_done = 0
    part_number = 1
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(part_size)
            if not chunk:
                break
            url = sign_part(upload_id, part_number)
            etag = put_to_presigned_url(url, chunk)
            completed.append({"ETag": etag, "partNumber": part_number})
            bytes_done += len(chunk)
            if on_progress:
                on_progress(bytes_done, total)
            part_number += 1

    if not completed:
        # Empty file: still need one empty part or single-shot; use empty part 1.
        url = sign_part(upload_id, 1)
        etag = put_to_presigned_url(url, b"")
        completed.append({"ETag": etag, "partNumber": 1})
        if on_progress:
            on_progress(0, 0)

    complete(upload_id, completed)
