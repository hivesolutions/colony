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

import os

from colony.base import legacy, exceptions

try: import Crypto.Cipher.AES
except ImportError: Crypto = None

BLOCK_SIZE = 16
""" The block size to be used for the post operation
should not be too small or security issues may arise """

class AesCipher(object):
    """
    The class responsible for a proper encryption
    and decryption system for the aes system.

    The aes include the padding infra-structure for
    according to PKCS #5.

    :see: http://tools.ietf.org/html/rfc2898
    """

    key = None
    """ The symmetric key to be use to encrypt
    messages under this aes cipher """

    block_size = BLOCK_SIZE
    """ The size of the encryption block to be
    used under this cipher instance """

    def __init__(self, key = None, block_size = BLOCK_SIZE):
        """
        Constructor of the class.

        :type key: String
        :param key: The symmetric key (secret) to be used
        in the aes encryption, in case it's not defined
        a new random key will be created.
        :type block_size: int
        :param block_size: The size of the encryption
        block to be used under this cipher instance, must
        be a multiple of eight.
        """

        self.key = key or os.urandom(block_size)
        self.block_size = block_size

    def encrypt(self, raw):
        """
        Encrypts the provided raw string value according
        to the aes and PKCS #5 specifications.

        :type raw: String
        :param raw: The raw string value to be used in
        the encryption process.
        :rtype: String
        :return: The encrypted string according to the aes
        cryptographic system in ecb mode.
        """

        if not Crypto:
            raise exceptions.OperationalError(message = "PyCrypto is not installed")

        raw = self.pad(raw)
        cipher = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_ECB)
        return cipher.encrypt(raw)

    def decrypt(self, encoded):
        """
        Decrypts the provided encoded (encrypted) string
        into the raw value.

        :type encoded: String
        :param encoded: The encrypted string to be used
        in the decryption process, should be padded according
        to the PKCS #5 schema.
        :rtype String
        :return: The decrypted string according to the aes
        cryptographic system in ecb mode.
        """

        if not Crypto:
            raise exceptions.OperationalError(message = "PyCrypto is not installed")

        cipher = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_ECB)
        decoded = cipher.decrypt(encoded)
        return self.unpad(decoded)

    def pad(self, value):
        """
        Adds the PKCS #5 padding to the provided value
        it should add all the extra padding values to it.

        :type value: String
        :param value: The base value for which the padded
        characters will be added.
        :rtype: String
        :return: The PKCS #5 padded string with the padding
        characters added to it.
        """

        remaining = self.block_size - len(value) % self.block_size
        padding = remaining * legacy.chr(remaining)
        return value + padding

    def unpad(self, value):
        """
        Removes the PKCS #5 padding from the provided value
        it should remove all the extra padding values from it.

        :type value: String
        :param value: The padded value from which all the
        extra padding characters.
        :rtype: String
        :return: The sanitized string without the extra
        padding characters.
        """

        last = value[-1]
        pad_size = ord(last)
        return value[:-pad_size]

    def get_key(self):
        """
        Retrieves the symmetric key that is currently set
        in the aes instance and that is going to be used
        for encryption and decryption, it should be of the
        same size as the block.

        :rtype: String
        :return: The symmetric key that is currently set
        in the aes instance.
        """

        return self.key

    def get_block_size(self):
        """
        Retrieves the size of the encryption block to be
        used for encryption and decryption, this value is
        used for both the generation of the key and for
        the padding creation.

        The integer value should be a multiple of eight.

        :rtype: int
        :return: The size of the encryption block to be
        used for encryption and decryption.
        """

        return self.block_size
