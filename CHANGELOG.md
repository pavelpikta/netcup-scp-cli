# Changelog

All notable changes to netcup CLI are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-07-17

### Added

- `users images upload` and `users isos upload`: S3 single-shot and multipart upload via SCP prepare/sign/complete APIs (`--multipart` / `--no-multipart`, `--part-size`).
- OpenAPI coverage inventory tests, S3 upload unit tests, and GitHub Actions CI (ruff + pytest on Python 3.9–3.12).

### Changed

- `APIClient` accepts JSON list bodies (needed for multipart complete).

## [1.2.0] - 2026-07-17

### Added

- `servers list --sort`: sort by `name` or `nickname` (prefix `-` for descending; repeatable for multi-field sort). Matches OpenAPI `2026.0703.095128`.

### Changed

- Bundled OpenAPI snapshot updated to **2026.0703.095128**.

## [1.0.0] - 2025-02-19

### Added

- Initial release.
- **Auth:** Device-code login, logout, revoke, show credentials path.
- **Servers:** list, get, power, set-hostname, set-nickname; disks (list, get, supported-drivers, set-driver, format); interfaces (list, get, create, update, delete); firewall (get, put, reapply, restore-copied-policies); ISO (get, attach, detach, images); snapshots (list, get, create, delete, export, revert, dryrun); rescue (get, activate, deactivate); metrics (cpu, disk, network, packet); logs list; image (flavours, setup); user-image setup; guest-agent get; storage-optimization start.
- **rDNS:** IPv4 and IPv6 get, set, delete.
- **Tasks:** list (with -q, --server-id, --state), get, cancel (PUT per OpenAPI).
- **Users:** info, get, update; failoverips v4/v6 list and route; firewall-policies list, get, create, update, delete; ssh-keys list, add, delete; vlans list, get, update; images list, delete, download-url; isos list, delete, download-url; logs list. Optional `--user-id` for all user-scoped commands.
- **VLANs:** Standalone `vlans get <vlan_id>`.
- **Maintenance:** ping (with Accept: text/plain to avoid 406), info.
- Credentials stored under `~/.config/netcup-cli/` (XDG_CONFIG_HOME). Only refresh token is stored; access token obtained on demand.
- Comprehensive README and production-oriented documentation.

### Fixed

- `maintenance ping` returning 406: request now sends `Accept: text/plain` for the ping endpoint.
- Task cancel: use PUT instead of POST per OpenAPI spec.

[1.3.0]: https://github.com/your-org/netcup-cli/releases/tag/v1.3.0
[1.2.0]: https://github.com/your-org/netcup-cli/releases/tag/v1.2.0
[1.0.0]: https://github.com/your-org/netcup-cli/releases/tag/v1.0.0
