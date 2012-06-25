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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 3370 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-06-17 06:18:55 +0100 (qua, 17 Jun 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import logging

try:
    import zmq
    boradcast = True
except:
    boradcast = False

class BroadcastHandler(logging.Handler):

    socket = None
    """ The current zero mq socket in used, this is
    the object to be used to broadcast the messages """

    def __init__(self, host = None, port = None):
        logging.Handler.__init__(self)

        if not boradcast: return

        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:5600")

    def flush(self):
        """
        Flushes the stream, this should be able to send
        the pending contents in the stream through it.
        """

        pass

    def emit(self, record):
        """
        Emit a record, to the output stream the record will
        be formated and then sent to the socket for broadcast.

        @type record: Record
        @param record: The log record to be sent through the
        output socket stream.
        """

        # in case the broadcast flag is unset returns
        # immediately can't be used
        if not boradcast: return

        try:
            # formats the record, retrieving the resulting
            # message string
            message = self.format(record)

            # in case the type of the message is unicode encodes it using the
            # default encoding for the transmission, then sends the message
            # through the socket
            if type(message) == types.UnicodeType: message = message.encode("utf-8")
            self.socket.send("colony %s" % message)

            # flushes the current stream
            self.flush()
        except:
            # handles the error in the proper manner
            self.handleError(record)
