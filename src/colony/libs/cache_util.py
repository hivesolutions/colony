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

class DataCacheMap(object):
    """
    Cache based map structure that may be used to store
    in memory data indexed to a certain name (may be used
    as file path) and to a certain (modification) timestamp.
    """

    data_map = {}
    """ The map associating the name of the entry with a
    tuple containing both the data of the entry and the
    timestamp from when it was last modified """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.data_map = {}

    def get(self, name, timestamp = None):
        """
        Retrieves the data associated with the provided
        name and with a timestamp value equivalent to the
        one provided (if any is provided).

        :type name: String
        :param name: The key name to retrieve the the associated
        data from the map.
        :type timestamp: float
        :param timestamp: The optional timestamp vale to be used
        in the validation of the retrieved item.
        :rtype: Object
        :return: The object retrieved from the data cache map.
        """

        # in case the name is not present in the data map the
        # control must be returned to the caller function
        if not name in self.data_map: return None

        # retrieves and unpacks the data tuple into the data
        # and the timestamp then if the timestamp value is provided
        # validates it agains the "just" retrieved timestamp
        data, _timestamp = self.data_map[name]
        if timestamp and timestamp > _timestamp: return None

        # returns the "resolved" cached data
        return data

    def add(self, name, data, timestamp):
        """
        Adds a new cache entry to the map, the provided name
        is used as the key in the indexing process.

        The entry must contain both the data and the timestamp
        for the association to be possible.

        :type name: String
        :param name: The name to be used as key in the map.
        :type data: String
        :param data: The data string to be used in the map.
        :type timestamp: float
        :param timestamp: The timestamp to be used in the indexing
        process, for validation purposes.
        """

        # creates a new tuple containing both the data and the
        # timestamp and then sets it in the data map for the
        # name key (will be latter retrieved base on that key)
        self.data_map[name] = (data, timestamp)

    def remove(self, name):
        """
        Removes the data item with the provided name from the map.

        :type name: String
        :param name: The name of the item to be removed, this is the
        reference key to be used in the removal process.
        """

        # in case the name is not present in the data map, returns
        # immediately otherwise proceed with the removal process
        if not name in self.data_map: return
        del self.data_map[name]
