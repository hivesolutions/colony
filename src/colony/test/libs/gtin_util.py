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

class GtinTest(colony.ColonyTestCase):
    """
    Class that tests the GTIN calculation method.
    """

    def test_calculate_control_value(self):
        """
        Tests the calculate control value function.
        """

        control_value = colony.calculate_control_value_gtin(629104150021)
        self.assertEqual(control_value, 3)

        control_value = colony.calculate_control_value_gtin(978097123458)
        self.assertEqual(control_value, 1)

        control_value = colony.calculate_control_value_gtin(978097123456)
        self.assertEqual(control_value, 7)

        control_value = colony.calculate_control_value_gtin(978097123457)
        self.assertEqual(control_value, 4)
