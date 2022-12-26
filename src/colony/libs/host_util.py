#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2022 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2022 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import socket
import struct

LOCAL_EXTENSION = ".local"
""" The local extension value """

LOOPBACK_IP4_ADDRESS = "127.0.0.1"
""" The loopback ip4 address """

LOOPBACK_IP6_ADDRESS = "::1"
""" The loopback ip6 address """

ALL_IP4_ADDRESS = "0.0.0.0"
""" The all ip4 address """

ALL_IP6_ADDRESS = "::0"
""" The all ip6 address """

DEFAULT_IP4_HOST = "google.com"
""" The default host to be used for ip4 queries """

DEFAULT_IP6_HOST = "ipv6.google.com"
""" The default host to be used for ip6 queries """

DEFAULT_PORT = 80
""" The default port to be used for queries """

def get_hostname():
    """"
    Retrieves the current base host name.

    :rtype: String
    :return: The current base host name.
    """

    # retrieves the current host name
    hostname = socket.gethostname()

    # returns the hostname
    return hostname

def get_hostname_local():
    """"
    Retrieves the current base host name.
    The host name is returned in local notation.

    :rtype: String
    :return: The current base host name (in local notation).
    """

    # retrieves the host name
    hostname = get_hostname()

    # checks if the hostname is of type local
    is_local_hostname = hostname.endswith(LOCAL_EXTENSION)

    # creates the "local" host name from the host name in
    # case it's necessary
    hostname_local = is_local_hostname and hostname or hostname + LOCAL_EXTENSION

    # returns the "local" host name
    return hostname_local

def get_address_ip4():
    """
    Retrieves the current "preferred" ip4 address.

    :rtype: String
    :return: The current "preferred" ip4 address.
    """

    # retrieves the ip4 addresses
    addresses_ip4 = get_addresses_ip4()

    # retrieves the "preferred" ip4 address
    preferred_address_ip4 = addresses_ip4 and addresses_ip4[0] or ALL_IP4_ADDRESS

    # returns the "preferred" ip4 address
    return preferred_address_ip4

def get_address_ip4_force(host = DEFAULT_IP4_HOST, port = DEFAULT_PORT):
    """
    Retrieves the current "preferred" ip4 address.
    This method uses a brute force hack that requires a remote
    connection. This method is way more compatible but should be used
    carefully as it requires an external "internet" connection.

    :type host: String
    :param host: The host to be used to retrieve the address.
    :type port: int
    :param port: The port to be used to retrieve the address.
    :rtype: String
    :return: The current "preferred" ip4 address.
    """

    # creates the force socket
    force_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # creates the address tuple
        address_tuple = (host, port)

        # connects to the host described in the
        # address tuple
        force_socket.connect(address_tuple)

        # retrieves the force socket address and port
        address, _port = force_socket.getsockname()
    except Exception:
        # sets the address as the default one
        address = ALL_IP4_ADDRESS
    finally:
        # closes the socket
        force_socket.close()

    # returns the address
    return address

def get_address_ip4_all():
    """
    Retrieves the current "preferred" ip4 address.
    This method uses all the possible methods to retrieve
    the ip4 address.
    Use this method carefully as it may require
    an external "internet" connection.

    :rtype: String
    :return: The current "preferred" ip4 address.
    """

    # retrieves the ip4 address using the "normal" method
    address_ip4 = get_address_ip4()

    # retrieves the ip4 address using the "force" method in
    # case the previous retrieval was not successful
    address_ip4 = address_ip4 == ALL_IP4_ADDRESS and get_address_ip4_force() or address_ip4

    # returns the ip4 address
    return address_ip4

def get_address_ip6():
    """
    Retrieves the current "preferred" ip6 address.

    :rtype: String
    :return: The current "preferred" ip6 address.
    """

    # retrieves the ip6 addresses
    addresses_ip6 = get_addresses_ip6()

    # retrieves the "preferred" ip6 address
    preferred_address_ip6 = addresses_ip6 and addresses_ip6[0] or ALL_IP6_ADDRESS

    # returns the "preferred" ip6 address
    return preferred_address_ip6

def get_address_ip6_force(host = DEFAULT_IP6_HOST, port = DEFAULT_PORT):
    """
    Retrieves the current "preferred" ip6 address.
    This method uses a brute force hack that requires a remote
    connection. This method is way more compatible but should be used
    carefully as it requires an external "internet" connection.

    :type host: String
    :param host: The host to be used to retrieve the address.
    :type port: int
    :param port: The port to be used to retrieve the address.
    :rtype: String
    :return: The current "preferred" ip6 address.
    """

    # creates the force socket
    force_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    try:
        # creates the address tuple
        address_tuple = (host, port)

        # connects to the host described in the
        # address tuple
        force_socket.connect(address_tuple)

        # retrieves the force socket address, port and
        # other values
        address, _port, _flow_info, _scope_id = force_socket.getsockname()
    except Exception:
        # sets the address as the default one
        address = ALL_IP6_ADDRESS
    finally:
        # closes the socket
        force_socket.close()

    # returns the address
    return address

def get_address_ip6_all():
    """
    Retrieves the current "preferred" ip6 address.
    This method uses all the possible methods to retrieve
    the ip6 address.
    Use this method carefully as it may require
    an external "internet" connection.

    :rtype: String
    :return: The current "preferred" ip6 address.
    """

    # retrieves the ip6 address using the "normal" method
    address_ip6 = get_address_ip6()

    # retrieves the ip6 address using the "force" method in
    # case the previous retrieval was not successful
    address_ip6 = address_ip6 == ALL_IP6_ADDRESS and get_address_ip6_force() or address_ip6

    # returns the ip6 address
    return address_ip6

def get_addresses_ip4():
    """
    Retrieves the list currently available ip4 addresses.

    :rtype: List
    :return: The list currently available ip4 addresses.
    """

    return get_addresses_family(socket.AF_INET, (LOOPBACK_IP4_ADDRESS,))

def get_addresses_ip6():
    """
    Retrieves the list currently available ip6 addresses.

    :rtype: List
    :return: The list currently available ip6 addresses.
    """

    return get_addresses_family(socket.AF_INET6, (LOOPBACK_IP6_ADDRESS,))

def get_addresses_family(filter_family, filter_addresses = []):
    """
    Retrieves the list of addresses available in the
    current machine for the given family of protocols.

    :type filter_family: int
    :param filter_family: The network family to be filtered.
    :type filter_addresses: List
    :param filter_addresses: The list of addresses to be ignored in
    the filtering.
    :rtype: List
    :return: The list of addresses available in the
    current machine for the given family of protocols.
    """

    # retrieves the current host address tuples
    address_tuples = get_address_tuples()

    # creates the list to hold the addresses
    addresses_list = []

    # iterates over all the address tuples
    for address_tuple in address_tuples:
        # unpacks the address tuple
        family, _socket_type, _protocol, _canonical_name, socket_address = address_tuple

        # in case the family is the one to be filtered
        if not family == filter_family:
            # continues the loop
            continue

        # extracts the socket host from the socket address
        socket_host = socket_address[0]

        # in case the socket host is present in the
        # filter addresses list
        if socket_host in filter_addresses:
            # continues the loop
            continue

        # adds the socket host to the list of addresses
        addresses_list.append(socket_host)

    # returns the addresses list
    return addresses_list

def get_address_tuples():
    """
    Retrieves the address tuples for the current
    host network interfaces.

    :rtype: List
    :return: The list of address tuples.
    """

    # retrieves the current host name
    hostname = socket.gethostname()

    # retrieves the address tuples
    address_tuples = socket.getaddrinfo(hostname, 0)

    # returns the address tuples
    return address_tuples

def ip4_address_from_network(ip4_address_network):
    """
    Converts the given ip4 network signed byte stream into
    an ip4 address string value.

    :type ip4_address_network: String
    :param ip4_address_network: The ip4 network signed byte stream
    to be converted.
    :rtype: String
    :return: The converted ip4 address string value.
    """

    # unpacks the data from the network signed byte stream
    ip4_address_data_bytes = struct.unpack("!4B", ip4_address_network)

    # creates and joins the data string to create the address
    ip4_address_data_string = [str(value) for value in ip4_address_data_bytes]
    ip4_address = ".".join(ip4_address_data_string)

    # returns the ip4 address
    return ip4_address

def ip4_address_to_network(ip4_address):
    """
    Converts the given ip4 address string value into an
    ip4 network signed byte stream.

    :type ip4_address: String
    :param ip4_address: The ip4 address string value to be
    converted.
    :rtype: String
    :return: The converted ip4 network signed byte stream.
    """

    # converts the ip4 address to a series of bytes
    ip4_address_data_string = ip4_address.split(".")
    ip4_address_data_bytes = [int(value) for value in ip4_address_data_string]

    # packs the series of bytes into a network signed byte stream
    ip4_address_data_bytes_length = len(ip4_address_data_bytes)
    ip4_address_data_bytes_length_string = str(ip4_address_data_bytes_length)
    ip4_address_network = struct.pack("!" + ip4_address_data_bytes_length_string + "B", *ip4_address_data_bytes)

    # returns the ip4 address network
    return ip4_address_network

def ip6_address_from_network(ip6_address_network):
    """
    Converts the given ip6 network signed short stream into
    an ip6 address string value.

    :type ip6_address_network: String
    :param ip6_address_network: The ip6 network signed short stream
    to be converted.
    :rtype: String
    :return: The converted ip6 address string value.
    """

    # unpacks the data from the network signed short stream
    ip6_address_data_shorts = struct.unpack("!8H", ip6_address_network)

    # creates and joins the data string to create the address
    ip6_address_data_string = ["%x" % value for value in ip6_address_data_shorts if value > 0]
    ip6_address = ":".join(ip6_address_data_string)

    # returns the ip6 address
    return ip6_address

def ip6_address_to_network(ip6_address):
    """
    Converts the given ip6 address string value into an
    ip6 network signed short stream.

    :type ip6_address: String
    :param ip6_address: The ip6 address string value to be
    converted.
    :rtype: String
    :return: The converted ip6 network signed short stream.
    """

    # converts the ip6 address to a series of shorts
    ip6_address_data_string = ip6_address.split(":")
    ip6_address_data_shorts = [int(value or "", 16) for value in ip6_address_data_string]

    # packs the series of shorts into a network signed short stream
    ip6_address_data_shorts_length = len(ip6_address_data_shorts)
    ip6_address_network = struct.pack("!" + ip6_address_data_shorts_length + "H", *ip6_address_data_shorts)

    # returns the ip6 address network
    return ip6_address_network
