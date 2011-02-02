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

plugin_path_list = ["plugins",
                    "%colony_demo_prefix_path%/pt.hive.colony.demo.plugins.twitter/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.bundles.plugins.base.bundles/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.build.automation/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.build.automation.extensions/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.build.automation.generator/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.build.automation.items/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.business/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.business.dummy/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.communication.push/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.communication.push_persistence/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.configuration/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.configuration.startup/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.data/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.data_converter/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.descriptor/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.distribution/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.distribution.helper/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.distribution.registry/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.dns.storage/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.document.pdf/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.dummy/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.encryption/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.format/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.http_log_analyzer/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.information/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.installation/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.javascript.file_handler/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.javascript.handlers/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.javascript.manager/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.language.wiki/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.mail.queue/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.mail.storage/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.access/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.access_control/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.authentication/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.authentication.logic/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.cache/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.client/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.client.apple_push/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.client.dns/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.client.http/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.client.ldap/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.client.smtp/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.console/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.distribution/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.gui/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.localization/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.localization.translation_bundle/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.log/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.mock/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.mod_python/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.packing/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.pool/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote.client/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote.client.jsonrpc/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote.client.xmlrpc/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote.jsonrpc/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote.rest/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote.rest.encoder/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.remote.xmlrpc/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.restricted/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.abecula/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.bittorrent/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.dns/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.http/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.irc/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.policy/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.pop/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.smtp/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.telnet/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.service.xmpp/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.storage/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.test/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.tasks/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.threads/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.main.work/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.messaging/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.misc/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.misc.gui/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.packaging/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.plugin_manager/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.printing/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.repository/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.resources/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.revision_control/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.crawler/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.index_persistence/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.index_serializer/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.indexer/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.interpreter/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.processor/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.provider/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.query_evaluator/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.query_interpreter/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.remote_service/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.search.scorer/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.security.captcha/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.service.bargania_rss/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.service.easypay/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.service.facebook/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.service.openid/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.service.twitter/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.service.web.mvc.encryption/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.service.yadis/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.specifications/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.system.installer/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.system.updater/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.template_engine/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.template.handler/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.util.javascript/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.validation/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.administration/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.entity_manager_administration/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.communication.push/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.communication.push_apple/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.encryption/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.manager/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.manager.page_item/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.monitor_item/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.panel_item/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.resources.base/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.resources.ui/src/colony/plugins",
                    "%colony_prefix_path%/pt.hive.colony.plugins.web.mvc.wiki/src/colony/plugins",
                    "%omni_prefix_path%/pt.hive.omni.plugins.base.data/src/omni/plugins",
                    "%omni_prefix_path%/pt.hive.omni.plugins.base.logic/src/omni/plugins",
                    "%omni_prefix_path%/pt.hive.omni.plugins.base.runtime/src/omni/plugins",
                    "%omni_prefix_path%/pt.hive.omni.plugins.extra.business/src/omni/plugins",
                    "%omni_prefix_path%/pt.hive.omni.plugins.migration/src/omni/plugins",
                    "%omni_prefix_path%/pt.hive.omni.plugins.migration.demo_data/src/omni/plugins",
                    "%omni_prefix_path%/pt.hive.omni.plugins.migration.diamante/src/omni/plugins",
                    "%hive_site_prefix_path%/pt.hive.hive_site.plugins.main/src/hive_site/plugins",
                    "%hive_blog_prefix_path%/pt.hive.hive_blog.plugins.main/src/hive_blog/plugins",
                    "%hive_development_prefix_path%/pt.hive.hive_development.plugins.media_dashboard/src/hive_development/plugins",
                    "%hive_development_prefix_path%/pt.hive.hive_development.plugins.media_dashboard.updater/src/hive_development/plugins",
                    "%hive_development_prefix_path%/pt.hive.hive_development.plugins.revision_control_analyzer/src/hive_development/plugins",
                    "%hive_development_prefix_path%/pt.hive.hive_development.plugins.service.media_dashboard/src/hive_development/plugins",
                    "%hive_development_prefix_path%/pt.hive.hive_development.plugins.task_registry/src/hive_development/plugins",
                    "%hive_openid_prefix_path%/pt.hive.hive_openid.plugins.main/src/hive_openid/plugins",
                    "%take_the_bill_prefix_path%/pt.hive.take_the_bill.plugins.demo_data/src/take_the_bill/plugins",
                    "%take_the_bill_prefix_path%/pt.hive.take_the_bill.plugins.main/src/take_the_bill/plugins",
                    "%a_la_carte_prefix_path%/pt.hive.a_la_carte.plugins.demo_data/src/a_la_carte/plugins",
                    "%a_la_carte_prefix_path%/pt.hive.a_la_carte.plugins.main/src/a_la_carte/plugins",
                    "%pecway_prefix_path%/pt.hive.pecway.plugins.main/src/pecway/plugins",
                    "%panzerini_prefix_path%/pt.hive.panzerini.plugins.dummy/src/panzerini/plugins",
                    "%panzerini_prefix_path%/pt.hive.panzerini.plugins.main.client.web_mvc/src/panzerini/plugins",
                    "%panzerini_prefix_path%/pt.hive.panzerini.plugins.main.logic/src/panzerini/plugins",
                    "%panzerini_prefix_path%/pt.hive.panzerini.plugins.main.websocket_handler/src/panzerini/plugins",
                    "%bargania_prefix_path%/com.bargania.bargania_site.plugins.main/src/bargania_site/plugins",
                    "%escolinhas_prefix_path%/pt.escolinhas.apple_push.notification_handler/src/escolinhas/plugins"]
""" The list of plugin paths """
