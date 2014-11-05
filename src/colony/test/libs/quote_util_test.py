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
        and correctly working. Uses a lot of languages to try
        to add complexity to the set of tests.
        """

        value = colony.quote("Hello World")
        self.assertEqual(value, "Hello%20World")

        value = colony.quote("Olá Mundo")
        self.assertEqual(value, "Ol%C3%A1%20Mundo")

        value = colony.quote("你好世界")
        self.assertEqual(value, "%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C")

    def test_unquote(self):
        """
        Validates and verifies that the unquoting (reverse operation)
        works using the default infra-structure.
        """

        value = colony.unquote("Hello%20World")
        self.assertEqual(value, "Hello World")

        value = colony.unquote("Ol%C3%A1%20Mundo")
        self.assertEqual(value, "Olá Mundo")

        value = colony.unquote("%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C")
        self.assertEqual(value, "你好世界")
