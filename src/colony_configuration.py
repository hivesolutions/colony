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

verbose = False
""" The verbose flag """

debug = True
""" The debug flag """

plugin_path_list = ["colony/plugins",
                    "%prefix_path%/pt.hive.colony.demo.plugins.twitter/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.build.automation/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.build.automation.extensions/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.build.automation.items/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.business/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.business.access_control/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.business.data/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.configuration.startup/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.distribution/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.distribution.helper/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.distribution.registry/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.dummy/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.eureka/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.eureka.mocks/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.io/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.javascript.file_handler/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.javascript.handlers/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.javascript.manager/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.access/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.console/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.distribution/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.gui/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.log/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.login/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.mod_python/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.pool/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.client/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.client.jsonrpc/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.client.pyro/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.client.soap/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.client.xmlrpc/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.jsonrpc/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.pyro/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.soap/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.remote.xmlrpc/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.restricted/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.service/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.service.http/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.service.irc/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.service.smtp/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.service.telnet/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.service.xmpp/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.test/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.tasks/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.threads/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.main.web/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.messaging/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.misc/src/colony/plugins;"  +\
                    "%prefix_path%/pt.hive.colony.plugins.misc.gui/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.plugin_manager/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.printing/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.resources/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.crawler/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.index_persistence/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.index_serializer/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.indexer/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.interpreter/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.provider/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.query_evaluator/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.query_interpreter/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.remote_service/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.search.scorer/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.system.updater/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.template_engine/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.template.administration/src/colony/plugins",
                    "%prefix_path%/pt.hive.colony.plugins.template.handler/src/colony/plugins",
                    "%prefix_path%/pt.hive.omni.plugins.base.data/src/omni/plugins",
                    "%prefix_path%/pt.hive.omni.plugins.base.logic/src/omni/plugins",
                    "%prefix_path%/pt.hive.omni.plugins.extra.business/src/omni/plugins",
                    "%prefix_path%/pt.hive.omni.plugins.pos.logic/src/omni/plugins"]
""" The list of plugin paths """
