from socket import AddressFamily, SocketKind
from typing import Any, Sequence

LOCAL_EXTENSION: str
LOOPBACK_IP4_ADDRESS: str
LOOPBACK_IP6_ADDRESS: str
ALL_IP4_ADDRESS: str
ALL_IP6_ADDRESS: str
DEFAULT_IP4_HOST: str
DEFAULT_IP6_HOST: str
DEFAULT_PORT: int

def get_hostname() -> str: ...
def get_hostname_local() -> str: ...
def get_address_ip4() -> str: ...
def get_address_ip4_force(host: str = ..., port: int = ...) -> str: ...
def get_address_ip4_all() -> str: ...
def get_address_ip6() -> str: ...
def get_address_ip6_force(host: str = ..., port: int = ...) -> str: ...
def get_address_ip6_all() -> str: ...
def get_addresses_ip4() -> Sequence[str]: ...
def get_addresses_ip6() -> Sequence[str]: ...
def get_addresses_family(
    filter_family: AddressFamily, filter_addresses: Sequence[str] = ...
) -> Sequence[str]: ...
def get_address_tuples() -> (
    Sequence[tuple[AddressFamily, SocketKind, int, str, Any]]
): ...
def ip4_address_from_network(ip4_address_network: str) -> str: ...
def ip4_address_to_network(ip4_address: str) -> str: ...
def ip6_address_from_network(ip6_address_network: str) -> str: ...
def ip6_address_to_network(ip6_address: str) -> str: ...
