# Changelog

All notable changes to netcup-scp-cli are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-17

First public release on [PyPI](https://pypi.org/project/netcup-scp-cli/) as **`netcup-scp-cli`**.

Built against SCP OpenAPI **2026.0703.095128**. Requires **Python 3.10+**. Console command: **`netcup`**. Import package: **`netcup_scp_cli`**. Credentials: `~/.config/netcup-scp-cli/`.

### Added

- **Auth:** OAuth2 device-code login, logout, revoke, show credentials path.
- **Servers:** list (filters + `--sort`), get, power, set-hostname, set-nickname; disks; interfaces; firewall; ISO; snapshots; rescue; metrics; logs; image flavours/setup; user-image setup; guest-agent; GPU driver URL; storage optimization.
- **rDNS:** IPv4 and IPv6 get, set, delete.
- **Tasks:** list (with filters), get, cancel.
- **Users:** info, get, update; failover IPs; firewall policies; SSH keys; VLANs; images/ISOs (list, delete, download-url, **upload** with S3 single-shot/multipart); logs. Optional `--user-id`.
- **VLANs:** Standalone `vlans get <vlan_id>`.
- **Maintenance:** ping, info.
- OpenAPI coverage inventory tests, upload/config unit tests, and GitHub Actions CI (lint + test on Python 3.10–3.14) with trusted publishing workflow.

### Notes

- Intentionally not wrapped: `GET /openapi` (bundled snapshot) and `POST /openapi/mcp` (explore-only).
- `maintenance ping` uses `Accept: text/plain` to avoid 406.
- Task cancel uses PUT per OpenAPI.

[1.0.0]: https://github.com/pavelpikta/netcup-cli/releases/tag/1.0.0
