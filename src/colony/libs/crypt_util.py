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

__revision__ = "$LastChangedRevision: 3219 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-05-26 11:52:00 +0100 (ter, 26 Mai 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import hashlib

MD5_CRPYT_SEPARATOR = "$"
""" The md5 crypt separator """

DEFAULT_MD5_CRYPT_MAGIC = "$1$"
""" The default md5 crypt magic value """

INTEGER_TO_ASCII_64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
""" The array of conversion from integer to ascii """

def md5_crypt(password, salt, magic = DEFAULT_MD5_CRYPT_MAGIC):
    """
    Runs the md5 crypt algorithm for the given password,
    salt and magic value.
    The magic value is set by default and should be changed
    carefully.

    @type password: String
    @param password: The password to be encrypted.
    @type salt: String
    @param salt: The salt to be used in encryption.
    @type magic: String
    @param magic: The magic value to be used in encryption.
    @rtype: String
    @return: The resulting md5 crypt value.
    """

    # creates the first hash value
    hash = hashlib.md5()

    # appends the password with the magic value and the salt
    # creating the "appended" value
    appended_value = password + magic + salt

    # updates the hash with the appended value
    hash.update(appended_value)

    # appends the password with the salt and the magic value
    # creating the "new appended" value
    appended_value = password + salt + password

    # retrieves the mixin hash from the appended value
    mixin_hash = hashlib.md5(appended_value)

    # retrieves the mixin digest from the
    # mixin hash
    mixin_digest = mixin_hash.digest()

    # retrieves the password length
    password_length = len(password)

    # iterates over the range of the password
    # length
    for index in range(password_length):
        hash.update(mixin_digest[index % 16])

    # retrieves the password length
    password_length = len(password)

    # retrieves the password (first) character
    password_character = password[0]

    # iterates while the password
    # length is still valid
    while password_length:
        # in case the password length (index)
        # is of type odd
        if password_length & 1:
            # updates the hash with the null value
            hash.update("\0")
        # otherwise the password length (index)
        # is of type even
        else:
            # updates the hash with the
            # password (first) character
            hash.update(password_character)

        # shifts the password length one
        # bit to the right
        password_length >>= 1

    # retrieves the has digest
    hash_digest = hash.digest()

    for index in range(1000):
        # creates the extras hash
        extra_hash = hashlib.md5()

        # in case the index is odd
        if index & 1:
            extra_hash.update(password)
        # in case the index is even
        else:
            extra_hash.update(hash_digest)

        # checks index for modulus three
        if index % 3:
            extra_hash.update(salt)

        # checks index for modulus seven
        if index % 7:
            extra_hash.update(password)

        # in case the index is odd
        if index & 1:
            extra_hash.update(hash_digest)
        # otherwise it must be even
        else:
            extra_hash.update(password)

        # retrieves the hash digest from
        # the extra hash
        hash_digest = extra_hash.digest()

    # creates the rearranged buffer
    rearranged_buffer = []

    # retrieves the various values from a pre-defined set of position
    for a, b, c in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
        value = ord(hash_digest[a]) << 16 | ord(hash_digest[b]) << 8 | ord(hash_digest[c])

        # iterates over the range of four
        for _index in range(4):
            # converts the value to ascii
            value_ascii = INTEGER_TO_ASCII_64[value & 0x3f]

            # adds the ascii value to the rearranged buffer
            rearranged_buffer.append(value_ascii)

            # shifts the value six bits to the right
            value >>= 6

    # retrieves the "last" value
    value = ord(hash_digest[11])

    # iterates over a two size range
    for _index in range(2):
        # converts the value to ascii
        value_ascii = INTEGER_TO_ASCII_64[value & 0x3f]

        # adds the ascii value to the rearranged buffer
        rearranged_buffer.append(value_ascii)

        # shifts the value six bits to the right
        value >>= 6

    # retrieves the rearranged from by joining
    # rearranged buffer
    rearranged = "".join(rearranged_buffer)

    # creates the md5 crypt value appending
    # the magic with the salt, the md5 crypt separator
    # and the rearranged value
    md5_crypt_value = magic + salt + MD5_CRPYT_SEPARATOR + rearranged

    # returns the md5 crypt value
    return md5_crypt_value
