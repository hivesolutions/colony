#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class QuoteTest(colony.ColonyTestCase):
    """
    Class that tests the various functions/methods related
    with the quoting/unquoting process of strings.
    """

    def test_quote(self):
        """
        Validates/verifies that the quoting support is complete
        and correctly working.
        """

        value = colony.quote("João Magalhães")
        self.assertEqual(value, "Jo%C3%A3o%20Magalh%C3%A3es")

        value = colony.quote("想更快瀏覽網頁")
        self.assertEqual(value, "%E6%83%B3%E6%9B%B4%E5%BF%AB%E7%80%8F%E8%A6%BD%E7%B6%B2%E9%A0%81")

    def test_unquote(self):
        """
        Validates and verifies that the unquoting (reverse operation)
        works using the default infra-structure.
        """

        value = colony.unquote("Jo%C3%A3o%20Magalh%C3%A3es")
        self.assertEqual(value, "João Magalhães")

        value = colony.unquote("%E6%83%B3%E6%9B%B4%E5%BF%AB%E7%80%8F%E8%A6%BD%E7%B6%B2%E9%A0%81")
        self.assertEqual(value, "想更快瀏覽網頁")
