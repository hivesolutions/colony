#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class BarcodeTest(colony.ColonyTestCase):
    """
    Class that tests the barcode generation methods.
    The series of tests should include the complete
    set of the barcode generation algorithms.
    """

    def test_2_to_5(self):
        """
        Tests the 2 to 5 barcode generation algorithm.
        """

        # encodes a "normal" even length based string value and asserts
        # that the encoded value is the expected one
        encoded_value = colony.encode_2_of_5("123456")
        self.assertEqual(encoded_value, "NnNnWnNwNnNnWwWnWnNwNnNwWnNwWwNnNnWnN")

        # encodes an odd length base string value and asserts that the
        # encoded value is the expected one (padded with the zero value)
        encoded_value = colony.encode_2_of_5("54321")
        self.assertEqual(encoded_value, "NnNnNwNnWwWnNnNwNwWnNnWnNwWnNnNnWwWnN")

    def test_code_128(self):
        """
        Tests the code 128 barcode generation algorithm.
        """

        # encodes a "normal" even length based string value and asserts
        # that the encoded value is the expected one
        encoded_value = colony.encode_code_128("123456")
        self.assertEqual(
            encoded_value,
            colony.legacy.u("\xcb123456/\xce", encoding = "unicode_escape")
        )

        # encodes a "normal" even length based string value and asserts
        # that the encoded value is the expected one, the used code set
        # is the a code set
        encoded_value = colony.encode_code_128("123456", "A")
        self.assertEqual(
            encoded_value,
            colony.legacy.u("\xcb123456/\xce", encoding = "unicode_escape")
        )

        # encodes a "normal" even length based string value and asserts
        # that the encoded value is the expected one, the used code set
        # is the b code set
        encoded_value = colony.encode_code_128("123456", "B")
        self.assertEqual(
            encoded_value,
            colony.legacy.u("\xcc1234560\xce", encoding = "unicode_escape")
        )

        # encodes a "normal" even length based string value and asserts
        # that the encoded value is the expected one, the used code set
        # is the c code set
        encoded_value = colony.encode_code_128("123456", "C")
        self.assertEqual(
            encoded_value,
            colony.legacy.u("\xcd,BXL\xce", encoding = "unicode_escape")
        )

    def test_code_39(self):
        """
        Tests the code 39 barcode generation algorithm.
        """

        # encodes a "normal" even length based string value and asserts
        # that the encoded value is the expected one
        encoded_value = colony.encode_code_39("123456")
        self.assertEqual(encoded_value, "*123456*")
