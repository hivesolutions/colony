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

        result = colony.quote("Hello World")
        self.assertEqual(result, "Hello%20World")

        result = colony.quote("Olá Mundo")
        self.assertEqual(result, "Ol%C3%A1%20Mundo")

        result = colony.quote("你好世界")
        self.assertEqual(result, "%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C")

    def test_quote_plus(self):
        """
        Plus version testing of the quoting operation, this test is
        analogous to the previous test.
        """

        result = colony.quote_plus("Hello World")
        self.assertEqual(result, "Hello+World")

        result = colony.quote_plus("Olá Mundo")
        self.assertEqual(result, "Ol%C3%A1+Mundo")

        result = colony.quote_plus("你好世界")
        self.assertEqual(result, "%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C")

    def test_unquote(self):
        """
        Validates and verifies that the unquoting (reverse operation)
        works using the default infra-structure. Will try to decode
        results from a variety of languages.
        """

        result = colony.unquote("Hello%20World")
        self.assertEqual(result, "Hello World")

        result = colony.unquote("Ol%C3%A1%20Mundo")
        self.assertEqual(result, "Olá Mundo")

        result = colony.unquote("%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C")
        self.assertEqual(result, "你好世界")

        result = colony.unquote("Hello%20World%GG")
        self.assertEqual(result, "Hello World%GG")

        result = colony.unquote("你好世界", strict = False)
        self.assertEqual(result, "你好世界")

        result = colony.unquote(b"\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c", strict = False)
        self.assertEqual(result, "你好世界")

        result = colony.unquote(colony.legacy.u("你好世界"), strict = False)
        self.assertEqual(result, "你好世界")

        self.assert_raises(
            UnicodeDecodeError,
            colony.unquote,
            b"\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c",
            strict = True
        )

        self.assert_raises(
            UnicodeEncodeError,
            colony.unquote,
            colony.legacy.u("你好世界"),
            strict = True
        )

    def test_unquote_plus(self):
        """
        Plus version testing of the unquoting operation, this test is
        analogous to the previous test.
        """

        result = colony.unquote_plus("Hello+World")
        self.assertEqual(result, "Hello World")

        result = colony.unquote_plus("Ol%C3%A1+Mundo")
        self.assertEqual(result, "Olá Mundo")

        result = colony.unquote_plus("%E4%BD%A0%E5%A5%BD%E4%B8%96%E7%95%8C")
        self.assertEqual(result, "你好世界")

        result = colony.unquote_plus("Hello+World%GG")
        self.assertEqual(result, "Hello World%GG")

        result = colony.unquote_plus("你好世界", strict = False)
        self.assertEqual(result, "你好世界")

        result = colony.unquote_plus(b"\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c", strict = False)
        self.assertEqual(result, "你好世界")

        result = colony.unquote_plus(colony.legacy.u("你好世界"), strict = False)
        self.assertEqual(result, "你好世界")

        self.assert_raises(
            UnicodeDecodeError,
            colony.unquote_plus,
            b"\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c",
            strict = True
        )

        self.assert_raises(
            UnicodeEncodeError,
            colony.unquote_plus,
            colony.legacy.u("你好世界"),
            strict = True
        )

    def test_url_encode(self):
        """
        Test for the URL encode operation that encodes the key to value
        attributes that is present in the query string for URLs.
        """

        items = (("message", "Hello World"), ("mensagem", "Olá Mundo"))

        result = colony.url_encode(attributes_list = items, plus_encoding = False)
        self.assertEqual(result, "message=Hello%20World&mensagem=Ol%C3%A1%20Mundo")

        result = colony.url_encode(attributes_list = items, plus_encoding = True)
        self.assertEqual(result, "message=Hello+World&mensagem=Ol%C3%A1+Mundo")
