#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 3219 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-05-26 11:52:00 +0100 (ter, 26 Mai 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

prefix_paths = {"development" : {"colony" : "../../",
                                 "omni" : "../../",
                                 "colony_demo" : "../../",
                                 "hive_site" : "../../",
                                 "hive_blog" : "../../",
                                 "hive_development" : "../../",
                                 "hive_openid" : "../../",
                                 "take_the_bill" : "../../",
                                 "a_la_carte" : "../../",
                                 "pecway" : "../../",
                                 "toolbox" : "../../",
                                 "panzerini" : "../../",
                                 "bargania" : "../../",
                                 "escolinhas" : "../../"},
                "repository_svn" : {"colony" : "../../",
                                    "omni" : "../../../../pt.hive.omni/trunk",
                                    "colony_demo" : "../../../../pt.hive.colony.demo/trunk",
                                    "hive_site" : "../../../../pt.hive.hive_site/trunk",
                                    "hive_blog" : "../../../../pt.hive.hive_blog/trunk",
                                    "hive_development" : "../../../../pt.hive.hive_development/trunk",
                                    "hive_openid" : "../../../../pt.hive.hive_openid/trunk",
                                    "take_the_bill" : "../../../../pt.hive.take_the_bill/trunk",
                                    "a_la_carte" : "../../../../pt.hive.a_la_carte/trunk",
                                    "pecway" : "../../../../pt.hive.pecway/trunk",
                                    "toolbox" : "../../../../pt.hive.toolbox/trunk",
                                    "panzerini" : "../../../../pt.hive.panzerini/trunk",
                                    "bargania" : "../../../../com.bargania/trunk",
                                    "escolinhas" : "../../../../pt.escolinhas/trunk"},
                "production" : {"colony" : "../../",
                                "omni" : "../../",
                                "colony_demo" : "../../",
                                "hive_site" : "../../",
                                "hive_blog" : "../../",
                                "hive_development" : "../../",
                                "hive_openid" : "../../",
                                "take_the_bill" : "../../",
                                "a_la_carte" : "../../",
                                "pecway" : "../../",
                                "toolbox" : "../../",
                                "panzerini" : "../../",
                                "bargania" : "../../",
                                "escolinhas" : "../../"}}
""" The prefix path maps """

library_path_list = ["%colony_prefix_path%/pt.hive.colony.language.generator/src/colony",
                     "%colony_prefix_path%/pt.hive.colony.language.settler/src/colony",
                     "%colony_prefix_path%/pt.hive.colony.language.wiki/src/colony"]
""" The list of library paths """

plugin_path_list = ["plugins"]
""" The list of plugin paths """

logger_path = "log"
""" The path to the logger directory """
