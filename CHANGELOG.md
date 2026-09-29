# Changelog

All notable changes to netcup-scp-cli are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Bundled `openapi.json` snapshot updated to **2026.0923.125530** (SCP release version bump only; no endpoint or schema changes vs **2026.0810.110900**).

## [1.0.1] - 2026-08-14

Aligned with SCP OpenAPI **2026.0810.110900**.

### Changed

- Bundled `openapi.json` snapshot updated to **2026.0810.110900**.
- `maintenance info` is marked deprecated (API removal by **31.12.2026**); the command is kept until then and prints a warning.
- API error messages now include the response body so status codes such as failover **429** are readable.

### Notes

- `User.secureMode` / `UserSave.secureMode` were removed from the spec. `users update --body` is unchanged (raw JSON).
- Failover IP routing is rate-limited: 10 requests per 5 minutes and 20 per 60 minutes (HTTP 429).

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

[Unreleased]: https://github.com/pavelpikta/netcup-cli/compare/1.0.1...HEAD
[1.0.1]: https://github.com/pavelpikta/netcup-cli/releases/tag/1.0.1
[1.0.0]: https://github.com/pavelpikta/netcup-cli/releases/tag/1.0.0
