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

class CountryTest(colony.ColonyTestCase):
    """
    Class that tests the country retrieval support.
    """

    def test_get(self):
        """
        Tests the get country function.
        """

        # verifies that a normal country name retrieval
        # succeeds, retrieving valid results
        result = colony.country_get("portugal")
        self.assertEqual(result, ("PT", "PRT", "620"))

        # verifies that a capitalized country name retrieval
        # still works, under the relaxed flag mode
        result = colony.country_get("Portugal")
        self.assertEqual(result, ("PT", "PRT", "620"))

        # verifies that a capitalized country name retrieval
        # fails if the relaxed flag is not set
        result = colony.country_get("Portugal", relaxed = False)
        self.assertEqual(result, (None, None, None))

        # verifies that a simplified country name retrieval
        # fails, retrieving invalid results
        result = colony.country_get("PT")
        self.assertEqual(result, (None, None, None))
