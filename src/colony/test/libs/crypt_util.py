#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class CryptTest(colony.ColonyTestCase):
    """
    Class that tests the various functions related
    with the cryptography utilities in Colony.
    """

    def test_md5_crypt(self):
        """
        Tests the MD5 crypt function using some simple values.
        """

        result = colony.md5_crypt("password", "salt")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "$1$salt$qJH7.N4xYta3aEG/dfqo/0")

        result = colony.md5_crypt("password", "01234567")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "$1$01234567$b5lh2mHyD2PdJjFfALlEz1")

    def test_md5_crypt_unicode(self):
        """
        Tests the MD5 crypt function using some simple values
        encoded in unicode.
        """

        result = colony.md5_crypt(colony.legacy.u("password"), colony.legacy.u("salt"))
        self.assertEqual(type(result), colony.legacy.UNICODE)
        self.assertEqual(result, "$1$salt$qJH7.N4xYta3aEG/dfqo/0")

        result = colony.md5_crypt(
            colony.legacy.u("password"), colony.legacy.u("01234567")
        )
        self.assertEqual(type(result), colony.legacy.UNICODE)
        self.assertEqual(result, "$1$01234567$b5lh2mHyD2PdJjFfALlEz1")

        result = colony.md5_crypt(colony.legacy.u("密码"), colony.legacy.u("01234567"))
        self.assertEqual(type(result), colony.legacy.UNICODE)
        self.assertEqual(result, "$1$01234567$MUE6EDF7dbbvoFo3c.Oj1.")
