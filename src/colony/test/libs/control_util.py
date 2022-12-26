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

class ControlTest(colony.ColonyTestCase):
    """
    Class that tests the control values calculation method.
    """

    def test_calculate_tax_number_control_value(self):
        """
        Tests the calculate tax number control value function.
        """

        control_value = colony.calculate_tax_number_control_value(23587818)
        self.assertEqual(control_value, 9)

        control_value = colony.calculate_tax_number_control_value(50860598)
        self.assertEqual(control_value, 9)

        control_value = colony.calculate_tax_number_control_value(50000175)
        self.assertEqual(control_value, 8)

        control_value = colony.calculate_tax_number_control_value(50464975)
        self.assertEqual(control_value, 2)

        control_value = colony.calculate_tax_number_control_value(98046859)
        self.assertEqual(control_value, 0)

    def test_calculate_id_number_control_value(self):
        """
        Tests the calculate id number control value function.
        """

        control_value = colony.calculate_id_number_control_value(12576330)
        self.assertEqual(control_value, 1)

        control_value = colony.calculate_tax_number_control_value(11873402)
        self.assertEqual(control_value, 4)

        control_value = colony.calculate_tax_number_control_value(52843401)
        self.assertEqual(control_value, 2)

        control_value = colony.calculate_tax_number_control_value(82523486)
        self.assertEqual(control_value, 7)
