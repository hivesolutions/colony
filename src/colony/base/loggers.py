#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import logging

from . import legacy

try:
    import zmq
    boradcast = True
except:
    boradcast = False

MAX_LENGTH = 10000
""" The maximum amount of messages that are kept in
memory until they are discarded, avoid a very large
number for this value or else a large amount of memory
may be used for logging purposes """

LEVELS = (
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL"
)
""" The sequence of levels from the least sever to the
most sever this sequence may be used to find all the
levels that are considered more sever that a level """

LEVEL_ALIAS = dict(
    DEBU = "DEBUG",
    WARN = "WARNING",
    INF = "INFO",
    ERR = "ERROR",
    CRIT = "CRITICAL"
)
""" Map defining a series of alias that may be used latter
for proper debug level resolution, standard compliant """

class BroadcastHandler(logging.Handler):
    """
    Logging handler that broadcasts the messages using the
    zero mq technology. It's useful for distributed logging
    situations where one wants to gather logging from a
    colony instance spread over a network space.
    """

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
            if type(message) == legacy.UNICODE: message = message.encode("utf-8")
            self.socket.send("colony %s" % message)

            # flushes the current stream
            self.flush()
        except:
            # handles the error in the proper manner
            self.handleError(record)

class MemoryHandler(logging.Handler):
    """
    Logging handler that is used to store information in
    memory so that anyone else may consult it latter as
    long as the execution session is the same.
    """

    def __init__(self, level = logging.NOTSET, max_length = MAX_LENGTH):
        logging.Handler.__init__(self, level = level)
        self.max_length = max_length
        self.messages = []
        self.messages_l = {}

    def get_messages_l(self, level):
        # in case the level is not found in the list of levels
        # it's not considered valid and so an empty list is returned
        try: index = LEVELS.index(level)
        except: return []

        # retrieves the complete set of levels that are considered
        # equal or less sever than the requested one
        levels = LEVELS[:index + 1]

        # creates the list that will hold the various message
        # lists associated with the current severity level
        messages_l = []

        # iterates over the complete set of levels considered
        # equal or less sever to add the respective messages
        # list to the list of message lists
        for level in levels:
            _messages_l = self.messages_l.get(level, [])
            self.messages_l[level] = _messages_l
            messages_l.append(_messages_l)

        # returns the complete set of messages lists that
        # have a level equal or less severe that the one
        # that has been requested by argument
        return messages_l

    def emit(self, record):
        # formats the current record according to the defined
        # logging rules so that we can used the resulting message
        # for any logging purposes
        message = self.format(record)

        # retrieves the level (as a string) associated with
        # the current record to emit and uses it to retrieve
        # the associated messages list
        level = record.levelname
        messages_l = self.get_messages_l(level)

        # inserts the message into the messages queue and in
        # case the current length of the message queue overflows
        # the one defined as maximum must pop message from queue
        self.messages.insert(0, message)
        messages_s = len(self.messages)
        if messages_s > self.max_length: self.messages.pop()

        # iterates over all the messages list included in the retrieve
        # messages list to add the logging message to each of them
        for _messages_l in messages_l:
            # inserts the message into the proper level specific queue
            # and in case it overflows runs the same pop operation as
            # specified also for the more general queue
            _messages_l.insert(0, message)
            messages_s = len(_messages_l)
            if messages_s > self.max_length: _messages_l.pop()

    def get_latest(self, count = None, level = None):
        count = count or 100
        level = level.upper() if level else level
        level = LEVEL_ALIAS.get(level, level)
        messages = self.messages_l.get(level, ()) if level else self.messages
        return messages[:count]
