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

import xml.dom.minidom

import colony

class XmlTest(colony.ColonyTestCase):
    """
    Test class for the complete set of functions associated
    with XML manipulation.
    """

    def test_xml_to_dict(self):
        """
        Verifies a series of conditions associated with XML to
        dictionary conversion.
        """

        result = colony.xml_to_dict("""<person>
            <name>Hello World</name>
            <age>32</age>
        </person>""")
        self.assertEqual(
            result,
            dict(
                person = dict(
                    name = "Hello World",
                    age = "32"
                )
            )
        )

        result = colony.xml_to_dict("""<person>
            <name>Hello World</name>
            <age>32</age>
            <address>
                <street>Wood Street</street>
                <city>London</city>
                <country>United Kingdom</country>
            </address>
        </person>""")
        self.assertEqual(
            result,
            dict(
                person = dict(
                    name = "Hello World",
                    age = "32",
                    address = dict(
                        street = "Wood Street",
                        city = "London",
                        country = "United Kingdom"
                    )
                )
            )
        )

        result = colony.xml_to_dict("""<person>
            <name>Hello World</name>
            <age>32</age>
            <address></address>
        </person>""")
        self.assertEqual(
            result,
            dict(
                person = dict(
                    name = "Hello World",
                    age = "32",
                    address = None
                )
            )
        )

        result = colony.xml_to_dict("""<person>
            <name>你好世界</name>
            <age>32</age>
        </person>""")
        self.assertEqual(
            result,
            dict(
                person = dict(
                    name = colony.legacy.u("你好世界"),
                    age = "32"
                )
            )
        )

        result = colony.xml_to_dict(
            xml.dom.minidom.parseString("""<person>
                <name>Hello World</name>
                <age>32</age>
            </person>""")
        )
        self.assertEqual(
            result,
            dict(
                person = dict(
                    name = "Hello World",
                    age = "32"
                )
            )
        )

    def test_dict_to_xml(self):
        """
        Verifies a series of conditions associated with dictionary
        to XML conversion
        """

        result = colony.dict_to_xml(dict(
            person = dict(
                name = "Hello World",
                age = "32"
            )
        ))
        self.assertEqual(result, "<person><age>32</age><name>Hello World</name></person>")

        result = colony.dict_to_xml(dict(
            person = dict(
                name = "Hello World",
                age = "32",
                address = dict(
                    street = "Wood Street",
                    city = "London",
                    country = "United Kingdom"
                )
            )
        ))
        self.assertEqual(result, "<person><address><city>London</city><country>United Kingdom</country><street>Wood Street</street></address><age>32</age><name>Hello World</name></person>")

        result = colony.dict_to_xml(dict(
            person = dict(
                name = "Hello World",
                age = "32",
                address = None
            )
        ))
        self.assertEqual(result, "<person><address></address><age>32</age><name>Hello World</name></person>")

        result = colony.dict_to_xml(dict(
            person = dict(
                name = "你好世界",
                age = "32"
            )
        ))
        self.assertEqual(result, colony.legacy.u("<person><age>32</age><name>你好世界</name></person>"))
