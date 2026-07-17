"""Tests for config path."""

from pathlib import Path

from netcup_scp_cli import config as cfg


def test_config_dir_uses_package_name(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert cfg._config_dir() == tmp_path / "netcup-scp-cli"
    assert cfg.credentials_path() == tmp_path / "netcup-scp-cli" / "credentials"
