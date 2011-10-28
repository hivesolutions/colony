#!/usr/bin/python
# -*- coding: utf-8 -*-

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

prefix_paths = {
    "default" : {
    },
    "workspace_eclipse" : {
        "colony" : "../..",
        "colony_extras" : "../..",
        "colony_language" : "../..",
        "colony_configuration" : "../..",
        "omni" : "../..",
        "omni_web" : "../..",
        "colony_web" : "../..",
        "colony_web_ui" : "../..",
        "colony_demo" : "../..",
        "colony_site" : "../..",
        "hive_site" : "../..",
        "hive_blog" : "../..",
        "hive_development" : "../..",
        "hive_openid" : "../..",
        "take_the_bill" : "../..",
        "take_the_bill_site" : "../..",
        "a_la_carte" : "../..",
        "pecway" : "../..",
        "products" : "../..",
        "products_extras" : "../..",
        "products_configuration" : "../..",
        "toolbox" : "../..",
        "panzerini" : "../..",
        "bargania" : "../..",
        "escolinhas" : "../..",
        "first_day" : "../.."
    },
    "repository_svn" : {
        "colony" : "../../../../../hive-main/pt.hive.colony.plugins/trunk",
        "colony_extras" : "../../../../../hive-main/pt.hive.colony.extras/trunk",
        "colony_language" : "../../../../../hive-main/pt.hive.colony.language/trunk",
        "colony_configuration" : "../../../../../hive-main/pt.hive.colony.configuration/trunk",
        "omni" : "../../../../../hive-main/pt.hive.omni/trunk",
        "omni_web" : "../../../../../hive-main/pt.hive.omni.web/trunk",
        "colony_web" : "../../../../../hive-main/pt.hive.colony.web/trunk",
        "colony_web_ui" : "../../../../../hive-main/pt.hive.colony.web.ui/trunk",
        "colony_demo" : "../../../../../hive-main/pt.hive.colony.demo/trunk",
        "colony_site" : "../../../../../hive-main/pt.hive.colony_site/trunk",
        "hive_site" : "../../../../../hive-local/pt.hive.hive_site/trunk",
        "hive_blog" : "../../../../../hive-local/pt.hive.hive_blog/trunk",
        "hive_development" : "../../../../../hive-local/pt.hive.hive_development/trunk",
        "hive_openid" : "../../../../../hive-local/pt.hive.hive_openid/trunk",
        "take_the_bill" : "../../../../../hive-local/pt.hive.take_the_bill/trunk",
        "take_the_bill_site" : "../../../../../hive-local/pt.hive.take_the_bill_site/trunk",
        "a_la_carte" : "../../../../../hive-local/pt.hive.a_la_carte/trunk",
        "pecway" : "../../../../../hive-local/pt.hive.pecway/trunk",
        "products" : "../../../../../hive-local/pt.hive.products/trunk",
        "products_extras" : "../../../../../hive-local/pt.hive.products.extras/trunk",
        "products_configuration" : "../../../../../hive-local/pt.hive.products.configuration/trunk",
        "toolbox" : "../../../../../hive-local-sandbox/pt.hive.toolbox/trunk",
        "panzerini" : "../../../../../hive-sandbox/pt.hive.panzerini/trunk",
        "bargania" : "../../../../../hive-local/com.bargania/trunk",
        "escolinhas" : "../../../../../hive-local/pt.escolinhas/trunk",
        "first_day" : "../../../../../hive-local/pt.first-day/trunk"
    },
    "repository_flat" : {
        "colony" : "../../../../pt.hive.colony.plugins/trunk",
        "colony_extras" : "../../../../pt.hive.colony.extras/trunk",
        "colony_language" : "../../../../pt.hive.colony.language/trunk",
        "colony_configuration" : "../../../../pt.hive.colony.configuration/trunk",
        "omni" : "../../../../pt.hive.omni/trunk",
        "omni_web" : "../../../../pt.hive.omni.web/trunk",
        "colony_web" : "../../../../pt.hive.colony.web/trunk",
        "colony_web_ui" : "../../../../pt.hive.colony.web.ui/trunk",
        "colony_demo" : "../../../../pt.hive.colony.demo/trunk",
        "colony_site" : "../../../../pt.hive.colony_site/trunk",
        "hive_site" : "../../../../pt.hive.hive_site/trunk",
        "hive_blog" : "../../../../pt.hive.hive_blog/trunk",
        "hive_development" : "../../../../pt.hive.hive_development/trunk",
        "hive_openid" : "../../../../pt.hive.hive_openid/trunk",
        "take_the_bill" : "../../../../pt.hive.take_the_bill/trunk",
        "take_the_bill_site" : "../../../../pt.hive.take_the_bill_site/trunk",
        "a_la_carte" : "../../../../pt.hive.a_la_carte/trunk",
        "pecway" : "../../../../pt.hive.pecway/trunk",
        "products" : "../../../../pt.hive.products/trunk",
        "products_extras" : "../../../../pt.hive.products.extras/trunk",
        "products_configuration" : "../../../../pt.hive.products.configuration/trunk",
        "toolbox" : "../../../../pt.hive.toolbox/trunk",
        "panzerini" : "../../../../pt.hive.panzerini/trunk",
        "bargania" : "../../../../com.bargania/trunk",
        "escolinhas" : "../../../../pt.escolinhas/trunk",
        "first_day" : "../../../../pt.first-day/trunk"
    },
    "repository_windows" : {
        "colony" : "../../../colony",
        "colony_extras" : "../../../colony_extras",
        "colony_language" : "../../../colony_language",
        "colony_configuration" : "../../../colony_configuration",
        "omni" : "../../../omni",
        "omni_web" : "../../../omni_web",
        "colony_web" : "../../../colony_web",
        "colony_web_ui" : "../../../colony_web_ui",
        "colony_demo" : "../../../colony_demo",
        "colony_site" : "../../../colony_site",
        "hive_site" : "../../../hive_site",
        "hive_blog" : "../../../hive_blog",
        "hive_development" : "../../../hive_development",
        "hive_openid" : "../../../hive_openid",
        "take_the_bill" : "../../../take_the_bill",
        "take_the_bill_site" : "../../../take_the_bill_site",
        "a_la_carte" : "../../../a_la_carte",
        "pecway" : "../../../pecway",
        "products" : "../../../products",
        "products_extras" : "../../../products_extras",
        "products_configuration" : "../../../products_configuration",
        "toolbox" : "../../../toolbox",
        "panzerini" : "../../../panzerini",
        "bargania" : "../../../bargania",
        "escolinhas" : "../../../escolinhas",
        "first_day" : "../../../first_day"
    }
}
""" The prefix path maps """

plugin_path_list = [
    "plugins"
]
""" The list of plugin paths """

library_path_list = [
    "libraries",
    "%colony_language_prefix_path%/pt.hive.colony.language.generator/src/colony",
    "%colony_language_prefix_path%/pt.hive.colony.language.settler/src/colony",
    "%colony_language_prefix_path%/pt.hive.colony.language.wiki/src/colony"
]
""" The list of library paths """

meta_path_list = [
    "%colony_configuration_prefix_path%/pt.hive.colony.configuration.all",
    "%colony_configuration_prefix_path%/pt.hive.colony.configuration.development",
    "%colony_configuration_prefix_path%/pt.hive.colony.configuration.extras",
    "%colony_configuration_prefix_path%/pt.hive.colony.configuration.production",
    "%products_configuration_prefix_path%/pt.hive.products.configuration.all",
    "%products_configuration_prefix_path%/pt.hive.products.configuration.development",
    "%products_configuration_prefix_path%/pt.hive.products.configuration.extras",
    "%products_configuration_prefix_path%/pt.hive.products.configuration.production"
]
""" The list of meta paths """

logger_path = "log"
""" The path to the logger directory """
