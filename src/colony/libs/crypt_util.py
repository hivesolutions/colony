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

import re
import hashlib

from colony.base import legacy

HASH_VALUE = "hash"
""" The hash value """

VALUE_VALUE = "value"
""" The value value """

PLAIN_VALUE = "plain"
""" The plain value """

MD5_VALUE = "md5"
""" The MD5 value """

SHA1_VALUE = "sha1"
""" The SHA1 value """

SHA256_VALUE = "sha256"
""" The SHA256 value """

MD5_CRPYT_SEPARATOR = "$"
""" The MD5 crypt separator """

DEFAULT_MD5_CRYPT_MAGIC = "$1$"
""" The default MD5 crypt magic value """

DEFAULT_HASH_SET = (MD5_VALUE, SHA1_VALUE, SHA256_VALUE)
""" The default hash set """

INTEGER_TO_ASCII_64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
""" The array of conversion from integer to ascii """

PASSWORD_VALUE_REGEX_VALUE = "^\{(?P<hash>\w+)\}(?P<value>.+)$"
""" The password value regex value """

NUMBER_REGEX_VALUE = "\d+"
""" The number regex value """

LETTER_LOWER_REGEX_VALUE = "[a-z]"
""" The letter lower regex value """

LETTER_UPPER_REGEX_VALUE = "[A-Z]"
""" The letter upper regex value """

SPECIAL_CHARACTER_REGEX_VALUE = ".[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]"
""" The special character regex value """

PASSWORD_VALUE_REGEX = re.compile(PASSWORD_VALUE_REGEX_VALUE)
""" The password value regex """

NUMBER_REGEX = re.compile(NUMBER_REGEX_VALUE)
""" The number regex """

LETTER_LOWER_REGEX = re.compile(LETTER_LOWER_REGEX_VALUE)
""" The letter lower regex """

LETTER_UPPER_REGEX = re.compile(LETTER_UPPER_REGEX_VALUE)
""" The letter upper regex """

SPECIAL_CHARACTER_REGEX = re.compile(SPECIAL_CHARACTER_REGEX_VALUE)
""" The special character regex """

def password_crypt(password, salt = "", hash_method = MD5_VALUE):
    """
    Encrypts the given password using the provided hash method.
    An optional salt may be provided for extra security.
    The generated hash is always defined in hexadecimal.

    :type password: String
    :param password: The password to be encrypted using
    the hash method.
    :type salt: String
    :param salt: The salt to be used during the encryption
    process.
    :type hash_method: String
    :param hash_method: The name of the hash method to be used
    for encryption.
    :rtype: String
    :return: The generated (complete) hash hexadecimal string.
    """

    # converts the name of the hash method to lower
    # case string
    hash_method_lower = hash_method.lower()

    # creates the password (word) from the
    # password an the salt
    password_word = password + salt

    # in case the hash method is of type plain
    if hash_method_lower == PLAIN_VALUE:
        # sets the hash value as the (base)
        # password word value (plain)
        hash_value = password_word
    # otherwise it must be a general hash function
    else:
        # creates the new hash object from the
        # hash method
        hash = hashlib.new(hash_method)

        # converts the password word into a bytes
        # based string (if required) and updates
        # the hash value with the password word
        password_word = legacy.bytes(password_word)
        hash.update(password_word)

        # retrieves the hash value from the
        # hex digest
        hash_value = hash.hexdigest()

    # creates the final password hash prepending the
    # hash method reference
    password_hash = "{" + hash_method_lower + "}" + hash_value

    # returns the password (final) hash
    # value (with the hash method prefix)
    return password_hash

def password_match(password_hash, password, salt = ""):
    """
    Checks if the given password hash value matched
    the given password using the given (optional) salt.
    The matching process executes the original hash function
    in order to check for same results.

    :type password_hash: String
    :param password_hash: The complete password hash hexadecimal string.
    :type password: String
    :param password: The base password for checking.
    :type salt: String
    :param salt: The base salt for checking.
    :rtype: bool
    :return: The result of the password match checking.
    """

    # tries to match the base password hash
    base_password_match = PASSWORD_VALUE_REGEX.match(password_hash)

    # retrieves the base password hash and value
    base_password_hash = base_password_match.group(HASH_VALUE)
    base_password_value = base_password_match.group(VALUE_VALUE)

    # creates the password (word) from the
    # password an the salt (secure work)
    password_word = password + salt

    # sets the initial value for the passwords
    # math result
    passwords_match = False

    # in case the base password hash is of type plain
    if base_password_hash == PLAIN_VALUE:
        # checks if both passwords match
        passwords_match = password_word == base_password_value
    # otherwise it must be a general hash function
    else:
        # creates the new hash object from the
        # base password hash (method)
        hash = hashlib.new(base_password_hash)

        # updates the hash value with the
        # password word, note that the value
        # is ensured to be a valid byte value
        password_word = legacy.bytes(password_word)
        hash.update(password_word)

        # retrieves the hash value from the
        # hex digest
        hash_value = hash.hexdigest()

        # checks if both password (hashes) match
        passwords_match = hash_value == base_password_value

    # returns if both password match
    return passwords_match

def password_strength(password):
    """
    Calculates the "theoretical" password strength
    from the given password.
    The returned value is an integer ranging from the lowest
    zero value (unsafest) to a limit value (safest).

    :type password: String
    :param password: The password to be measured for strength.
    :rtype: int
    :return: An integer describing the strength
    level of the given password.
    """

    # starts the strength value
    # counter to the minimum value (zero)
    strength_value = 0

    # retrieves the length of the password
    password_length = len(password)

    # in case the password is not set
    # (empty password)
    if password_length < 1:
        # returns the strength value
        # immediately
        return strength_value

    # increments the strength value
    strength_value += 1

    # in case the password length is less
    # than a minimum of four
    if password_length < 4:
        # returns the strength value
        # immediately
        return strength_value

    # in case the password length is more
    # or equal to eight
    if password_length >= 8:
        # increments the strength value
        strength_value += 1

    # in case the password length is more
    # or equal to eleven
    if password_length >= 11:
        # increments the strength value
        strength_value += 1

    # in case the password contains at least
    # a number in it
    if NUMBER_REGEX.search(password):
        # increments the strength value
        strength_value += 1

    # in case the password contains both lower case and
    # upper case letters
    if LETTER_LOWER_REGEX.search(password) and LETTER_UPPER_REGEX.search(password):
        # increments the strength value
        strength_value += 1

    # in case the password contains special characters
    # in it (extra security)
    if SPECIAL_CHARACTER_REGEX.search(password):
        # increments the strength value
        strength_value += 1

    # returns the strength value
    return strength_value

def md5_crypt(password, salt, magic = DEFAULT_MD5_CRYPT_MAGIC):
    """
    Runs the MD5 crypt algorithm for the given password,
    salt and magic value.
    The magic value is set by default and should be changed
    carefully.

    :type password: String
    :param password: The password to be encrypted.
    :type salt: String
    :param salt: The salt to be used in encryption.
    :type magic: String
    :param magic: The magic value to be used in encryption.
    :rtype: String
    :return: The resulting MD5 crypt value.
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

    # creates the MD5 crypt value appending
    # the magic with the salt, the MD5 crypt separator
    # and the rearranged value
    md5_crypt_value = magic + salt + MD5_CRPYT_SEPARATOR + rearranged

    # returns the MD5 crypt value
    return md5_crypt_value

def generate_hash_digest_map(file_path, hash_set = DEFAULT_HASH_SET):
    """
    Generates a map containing a set of hash digests generate
    from the file contained in the given file path.
    The set of hash function to be used may be controlled using the
    hash set parameter.

    :type file_path: String
    :param file_path: The path to the file to be used for hash
    digest calculation.
    :type hash_set: Tuple
    :param hash_set: The set of hash functions to be used.
    :rtype: Dictionary
    :return: The map containing the hash digest values for the file.
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
