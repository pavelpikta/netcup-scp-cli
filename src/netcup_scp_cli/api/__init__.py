"""API resource modules for SCP."""

from .maintenance import get_maintenance, ping
from .rdns import (
    rdns_delete_ipv4,
    rdns_delete_ipv6,
    rdns_get_ipv4,
    rdns_get_ipv6,
    rdns_set_ipv4,
    rdns_set_ipv6,
)
from .servers import (
    server_get,
    server_list,
    server_patch,
)
from .tasks import task_cancel, task_get, task_list
from .users import user_get, user_info

__all__ = [
    "ping",
    "get_maintenance",
    "server_list",
    "server_get",
    "server_patch",
    "rdns_get_ipv4",
    "rdns_set_ipv4",
    "rdns_delete_ipv4",
    "rdns_get_ipv6",
    "rdns_set_ipv6",
    "rdns_delete_ipv6",
    "task_list",
    "task_get",
    "task_cancel",
    "user_info",
    "user_get",
]
