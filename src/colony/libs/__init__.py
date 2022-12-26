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

from . import aes_util
from . import bank_util
from . import barcode_util
from . import cache_util
from . import call_util
from . import control_util
from . import country_util
from . import crypt_util
from . import encode_util
from . import file_util
from . import gtin_util
from . import host_util
from . import import_util
from . import lazy_util
from . import list_util
from . import logging_util
from . import map_util
from . import math_util
from . import number_util
from . import object_util
from . import observer_util
from . import os_util
from . import path_util
from . import protection_util
from . import quote_util
from . import round_util
from . import scheduling_util
from . import size_util
from . import stack_util
from . import string_buffer_util
from . import string_util
from . import structures_util
from . import test_util
from . import time_util
from . import update_thread_util
from . import verify_util
from . import version_util
from . import visitor_util
from . import xml_util

from .aes_util import AesCipher
from .barcode_util import encode_2_of_5, encode_code_128, encode_code_39
from .cache_util import DataCacheMap
from .call_util import execute_retries, call_safe
from .control_util import calculate_tax_number_control_value, calculate_id_number_control_value
from .country_util import COUNTRIES, country_get
from .crypt_util import password_crypt, password_match, password_strength, md5_crypt,\
    generate_hash_digest_map
from .encode_util import encode_two_complement_string, decode_two_complement_string
from .file_util import FileRotator, FileContext, TransactionContext, FileImmediateContext,\
    FileTransactionContext
from .host_util import get_hostname, get_hostname_local, get_address_ip4, get_address_ip4_force,\
    get_address_ip4_all, get_address_ip6, get_address_ip6_force, get_address_ip6_all,\
    get_addresses_ip4, get_addresses_ip6, get_addresses_family, get_address_tuples,\
    ip4_address_from_network, ip4_address_to_network, ip6_address_from_network,\
    ip6_address_to_network
from .import_util import reload_import
from .lazy_util import LazyClass, LazyIteratorClass, is_lazy, Lazy, LazyIterator
from .list_util import list_intersect, list_extend, list_no_duplicates
from .logging_util import getLogger, getLevelName, DummyLogger, StreamHandler, Formatter
from .map_util import map_clean, map_get, map_copy, map_copy_deep, map_duplicate,\
    map_remove, map_extend, map_flatten, map_check_parameters, map_get_value_cast,\
    map_get_values, map_output, map_normalize
from .math_util import ceil_integer, greatest_common_divisor, fast_exponentiation,\
    item_set_total, item_set_percentage
from .number_util import get_number_length, get_digit, to_fixed
from .object_util import object_attribute_names, object_attribute_values, object_flatten,\
    object_print_list, object_print
from .observer_util import unique, notify, message, action, progress, register_g,\
    unregister_g, notify_g
from .os_util import kill_process
from .path_util import SEPARATOR, normalize_path, align_path, copy_directory, copy_link, copy_file,\
    remove_directory, link, link_copy, ensure_file_path, is_parent_path, relative_path
from .protection_util import public, Protected
from .quote_util import quote, quote_plus, unquote, unquote_plus, url_encode
from .round_util import roundi, rounds, roundt, round_apply, round_unapply, round_is_new
from .scheduling_util import SCHEDULING_MAX, Scheduler
from .size_util import size_round_unit
from .stack_util import get_instance_module_directory, get_call_module_directory
from .string_buffer_util import StringBuffer
from .string_util import xor_string_value, to_underscore, to_camelcase, pluralize,\
    capitalize_all, join
from .structures_util import Decimal, JournaledList, OrderedMap, OrderedMapIterator,\
    MultipleValueMap, FormatTuple, FileReference, is_dictionary
from .test_util import ColonyTestCase
from .time_util import SIMPLE_VALUE, BASIC_VALUE, EXTENDED_VALUE, EXTENDED_SIMPLE_VALUE,\
    MINIMIZE_MULTIPLE, MINIMIZE_UNIQUE, format_seconds_smart, format_seconds, timestamp_datetime
from .update_thread_util import UpdateThread
from .verify_util import verify, verify_equal, verify_not_equal, verify_type, verify_many
from .version_util import version_cmp, version_is_concrete
from .visitor_util import visit, dispatch_visit
from .xml_util import xml_to_dict, dict_to_xml

from .bank_util import calculate_control_value as calculate_control_value_bank
from .gtin_util import calculate_control_value as calculate_control_value_gtin

from .import_util import __import__
