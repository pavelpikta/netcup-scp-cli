"""CLI smoke tests for users images/isos upload."""

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from netcup_scp_cli.cli.main import cli


def test_images_upload_cli(tmp_path: Path) -> None:
    f = tmp_path / "img.bin"
    f.write_bytes(b"data")
    runner = CliRunner()
    with (
        patch("netcup_scp_cli.cli.users_resources_cmd.resolve_user_id", return_value=7),
        patch("netcup_scp_cli.cli.users_resources_cmd.user_image_upload") as upload,
    ):
        result = runner.invoke(cli, ["users", "images", "upload", "k1", str(f), "--no-multipart"])
    assert result.exit_code == 0, result.output
    assert "OK" in result.output
    upload.assert_called_once()
    args, kwargs = upload.call_args
    assert args[0] == 7
    assert args[1] == "k1"
    assert kwargs["use_multipart"] is False


def test_isos_upload_cli(tmp_path: Path) -> None:
    f = tmp_path / "os.iso"
    f.write_bytes(b"iso")
    runner = CliRunner()
    with (
        patch("netcup_scp_cli.cli.users_resources_cmd.resolve_user_id", return_value=7),
        patch("netcup_scp_cli.cli.users_resources_cmd.user_iso_upload") as upload,
    ):
        result = runner.invoke(cli, ["users", "isos", "upload", "k2", str(f), "--multipart"])
    assert result.exit_code == 0, result.output
    upload.assert_called_once()
    assert upload.call_args.kwargs["use_multipart"] is True
