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

from colony.base import legacy

def xml_to_dict(data):
    """
    Converts the provided linear XML string value into
    a dictionary that represents the same hierarchy.

    The conversion strategy is only applicable to simple
    hierarchical XML structures.

    :type data: String/Node
    :param data: The XML string (or XML node) to be used in
    the (to dictionary) conversion.
    :rtype: Dictionary
    :return: The dictionary representation of the XML data.
    """

    if isinstance(data, xml.dom.Node): node = data
    else: node = xml.dom.minidom.parseString(data)
    return _node_to_dict(node)

def dict_to_xml(contents, encoding = "utf-8"):
    """
    Converts the provided dictionary structure into an
    XML string string in a recursive fashion.

    :type contents: Dictionary
    :param contents: The dictionary that is going to be
    converted into a linear XML string.
    :type encoding: String
    :param encoding: The string encoding to be used if
    necessary to decode byte base string elements.
    :rtype: String
    :return: The final XML string value representing the
    given dictionary in a linear fashion.
    """

    buffer = []
    for key in sorted(legacy.keys(contents)):
        value = contents[key]
        if isinstance(value, dict):
            value = dict_to_xml(value, encoding = encoding)
        elif legacy.is_bytes(value):
            value = value.decode(encoding)
        elif value == None:
            value = legacy.u("")
        buffer.append(legacy.u("<%s>%s</%s>") % (key, value, key))
    return legacy.u("").join(buffer)

def _node_to_dict(node):
    contents = None
    for _node in node.childNodes:
        if _node.nodeType == xml.dom.Node.ELEMENT_NODE:
            if not contents: contents = dict()
            contents[_node.nodeName] = _node_to_dict(_node)
        if _node.nodeType == xml.dom.Node.TEXT_NODE and _node.data.strip():
            contents = _node.data.strip()
    return contents
