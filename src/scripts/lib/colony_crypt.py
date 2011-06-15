#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 10411 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-09-14 19:26:03 +0100 (ter, 14 Set 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import hashlib

MD5_VALUE = "md5"
""" The md5 value """

SHA1_VALUE = "sha1"
""" The sha1 value """

SHA256_VALUE = "sha256"
""" The sha256 value """

DEFAULT_HASH_SET = (MD5_VALUE, SHA1_VALUE, SHA256_VALUE)
""" The default hash set """

def generate_hash_digest_map(file_path, hash_set = DEFAULT_HASH_SET):
    """
    Generates a map containing a set of hash digests generate
    from the file contained in the given file path.
    The set of hash function to be used may be controlled using the
    hash set parameter.

    @type file_path: String
    @param file_path: The path to the file to be used for hash
    digest calculation.
    @type hash_set: Tuple
    @param hash_set: The set of hash functions to be used.
    @rtype: Dictionary
    @return: The map containing the hash digest values for the file.
    """

    # creates the list to hold the various
    # hash objects
    hash_list = []

    # iterates over the hash set
    # to create the various hash objects
    for hash_name in hash_set:
        # creates the hash object and adds
        # it to the list of hash objects
        hash = hashlib.new(hash_name)
        hash_list.append(hash)

    # opens the file for read
    file = open(file_path, "rb")

    try:
        # iterates continuously
        while True:
            # reads "some" file contents
            file_contents = file.read(4096)

            # in case the file contents are
            # not valid (end of file)
            if not file_contents:
                # breaks the loop
                break

            # iterates over all the hash objects
            # in the hash list to update them
            for hash in hash_list:
                # updates the hash object
                # with the file contents
                hash.update(file_contents)
    finally:
        # closes the file
        file.close()

    # creates the map to hold the various
    # hash digests
    hash_digest_map = {}

    # iterates over all the hash objects
    # in the hash list to retrieve the digest
    # and update the hash digest map
    for hash in hash_list:
        # retrieves the name of the hash (function)
        hash_name = hash.name

        # retrieves the hash (hexadecimal) digest
        hash_digest = hash.hexdigest()

        # updates the hash digest map with the
        # new hash digest
        hash_digest_map[hash_name] = hash_digest

    # returns the hash digest map
    return hash_digest_map
