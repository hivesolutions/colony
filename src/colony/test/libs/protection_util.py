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

class ProtectionTest(colony.ColonyTestCase):
    """
    Test case class responsible for the management of the
    tests for the protection utilities.
    """

    def test_access(self):
        """
        Test that verifies the access to the public and
        the non possible access to the private methods.
        """

        mock = ProtectionMock()

        result = mock.public()
        self.assertEqual(result, "public")
        self.assert_raises(AttributeError, getattr, mock, "private")
        self.assert_raises(AttributeError, getattr, mock, "protected")

        result = mock.private_hack()
        self.assertEqual(result, "private")

class ProtectionMock(colony.Protected):
    """
    Mock class to be used in the testing of protected
    attributes, should inherit from the (abstract) class
    responsible for the "protection".
    """

    name = "protected"
    """ The name attribute, should be protected by
    the protected infra-structure """

    @colony.public
    def public(self):
        return "public"

    def private(self):
        return "private"

    @colony.public
    def private_hack(self):
        return self.private()
