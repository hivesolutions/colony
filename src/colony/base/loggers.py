#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import time
import socket
import logging
import itertools
import datetime
import threading
import collections

from . import config
from . import legacy
from . import information

try:
    import zmq

    broadcast = True
except ImportError:
    broadcast = False

MAX_LENGTH = 10000
""" The maximum amount of messages that are kept in
memory until they are discarded, avoid a very large
number for this value or else a large amount of memory
may be used for logging purposes """

MAX_LENGTH_LOGSTASH = 256
""" The maximum amount of messages that are kept in
memory until they are flushed, avoid a very large
number for this value or else a large amount of memory
may be used for logging purposes """

TIMEOUT_LOGSTASH = 30.0
""" The maximum amount of time in between flush
operations in the logstash handler """

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
""" The sequence of levels from the least sever to the
most sever this sequence may be used to find all the
levels that are considered more sever that a level """

LEVEL_ALIAS = dict(
    DEBU="DEBUG", WARN="WARNING", INF="INFO", ERR="ERROR", CRIT="CRITICAL"
)
""" Map defining a series of alias that may be used latter
for proper debug level resolution, standard compliant """


class BroadcastHandler(logging.Handler):
    """
    Logging handler that broadcasts the messages using the
    ZeroMQ technology. It's useful for distributed logging
    situations where one wants to gather logging from a
    colony instance spread over a network space.

    :see: https://zeromq.org
    """

    socket = None
    """ The current ZeroMQ socket in used, this is
    the object to be used to broadcast the messages """

    def __init__(self, host=None, port=None):
        logging.Handler.__init__(self)

        if not broadcast:
            return

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
        be formatted and then sent to the socket for broadcast.

        :type record: Record
        :param record: The log record to be sent through the
        output socket stream.
        """

        # in case the broadcast flag is unset returns
        # immediately can't be used
        if not broadcast:
            return

        try:
            # formats the record, retrieving the resulting
            # message string
            message = self.format(record)

            # in case the type of the message is unicode encodes it using the
            # default encoding for the transmission, then sends the message
            # through the socket
            if type(message) == legacy.UNICODE:
                message = message.encode("utf-8")
            self.socket.send(b"colony %s" % message)

            # flushes the current stream
            self.flush()
        except Exception:
            # handles the error in the proper manner
            self.handleError(record)


class MemoryHandler(logging.Handler):
    """
    Logging handler that is used to store information in
    memory so that anyone else may consult it latter as
    long as the execution session is the same.
    """

    def __init__(self, level=logging.NOTSET, max_length=MAX_LENGTH):
        logging.Handler.__init__(self, level=level)
        self.max_length = max_length
        self.messages = collections.deque()
        self.messages_l = dict()

    def get_messages_l(self, level):
        # in case the level is not found in the list of levels
        # it's not considered valid and so an empty list is returned
        try:
            index = LEVELS.index(level)
        except Exception:
            return collections.deque()

        # retrieves the complete set of levels that are considered
        # equal or more severe than the requested one
        levels = LEVELS[: index + 1]

        # creates the list that will hold the various message
        # lists associated with the current severity level
        messages_l = collections.deque()

        # iterates over the complete set of levels considered
        # equal or less sever to add the respective messages
        # list to the list of message lists
        for level in levels:
            _messages_l = self.messages_l.get(level, None)
            if _messages_l == None:
                _messages_l = collections.deque()
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
        self.messages.appendleft(message)
        messages_s = len(self.messages)
        if messages_s > self.max_length:
            self.messages.pop()

        # iterates over all the messages list included in the retrieve
        # messages list to add the logging message to each of them
        for _messages_l in messages_l:
            # inserts the message into the proper level specific queue
            # and in case it overflows runs the same pop operation as
            # specified also for the more general queue
            _messages_l.appendleft(message)
            messages_s = len(_messages_l)
            if messages_s > self.max_length:
                _messages_l.pop()

    def clear(self):
        self.messages = collections.deque()
        self.messages_l = dict()

    def get_latest(self, count=None, level=None):
        count = count or 100
        is_level = level and not legacy.is_string(level)
        if is_level:
            level = logging.getLevelName(level)
        level = level.upper() if level else level
        level = LEVEL_ALIAS.get(level, level)
        messages = self.messages_l.get(level, []) if level else self.messages
        slice = itertools.islice(messages, 0, count)
        return list(slice)

    def flush_to_file(self, path, count=None, level=None, reverse=True, clear=True):
        messages = self.get_latest(level=level, count=count or 65536)
        if not messages:
            return
        if reverse:
            messages.reverse()
        is_path = isinstance(path, legacy.STRINGS)
        file = open(path, "wb") if is_path else path
        try:
            for message in messages:
                message = legacy.bytes(message, "utf-8", force=True)
                file.write(message + b"\n")
        finally:
            if is_path:
                file.close()
        if clear:
            self.clear()


class LogstashHandler(logging.Handler):

    def __init__(
        self,
        level=logging.NOTSET,
        max_length=MAX_LENGTH_LOGSTASH,
        timeout=TIMEOUT_LOGSTASH,
        api=None,
    ):
        logging.Handler.__init__(self, level=level)
        if not api:
            api = self._build_api()
        self.messages = collections.deque()
        self.max_length = max_length
        self.timeout = timeout
        self.api = api
        self._last_flush = time.time()

    @classmethod
    def is_ready(cls):
        try:
            import logstash
        except ImportError:
            return False
        if not config.conf("LOGGING_LOGSTASH", False, cast=bool):
            return False
        return True

    def emit(self, record, raise_e=False):
        # verifies if the API structure is defined and set and if
        # that's not the case returns immediately
        if not self.api:
            return

        # in case the record to be emitted has been marked as being
        # part of a stack (traceback) then ignores it (noise)
        if hasattr(record, "stack") and record.stack:
            return

        # retrieves the current date time value as an utc value
        # and then formats it according to the provided format string
        message = self.format(record)

        # creates the log record structure that is going to be sent
        # to the logstash infra-structure, this should represent a
        # proper structure ready to be debugged
        now = datetime.datetime.utcnow()
        now_s = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # tries to build the right version of the `meta` information
        # present in the record using either the structure `meta`
        # value or the lazy evaluation of the `meta_c` method
        if hasattr(record, "meta"):
            meta = record.meta
        elif hasattr(record, "meta_c"):
            meta = dict()
            for callable in record.meta_c:
                try:
                    ctx = callable()
                except Exception:
                    if raise_e:
                        raise
                    ctx = dict()
                meta.update(ctx)
        else:
            meta = None

        log = {
            "@timestamp": now_s,
            "message_fmt": message,
            "logger": record.name,
            "message": record.message,
            "level": record.levelname,
            "path": record.pathname,
            "lineno": record.lineno,
            "meta": getattr(record, "meta", None),
            "host": socket.gethostname(),
            "hostname": socket.gethostname(),
            "tid": threading.current_thread().ident,
            "pid": os.getpid() if hasattr(os, "getpid") else -1,
            "version": information.VERSION,
            "colony": True,
        }
        if not meta == None:
            log["meta"] = meta

        self.messages.append(log)
        message_overflow = len(self.messages) >= self.max_length
        time_overflow = time.time() - self._last_flush > self.timeout
        should_flush = message_overflow or time_overflow
        if should_flush:
            try:
                self.flush(raise_e=raise_e)
            except Exception:
                if raise_e:
                    raise

    def flush(self, force=False, raise_e=False):
        logging.Handler.flush(self)

        # verifies if the API structure is defined and set and if
        # that's not the case returns immediately
        if not self.api:
            return

        # in case the force flag is not set and there are no messages
        # to be flushed returns immediately (nothing to be done)
        messages = self.messages
        if not messages and not force:
            return

        # clears the current set of messages and updates the last flush timestamp
        # does this before the actual flush operation to avoid duplicated messages
        self.messages = []
        self._last_flush = time.time()

        # posts the complete set of messages to logstash, notice that this is a blocking
        # call and may take some time to be completed
        self.api.log_bulk(messages, tag="default", raise_e=raise_e)

    def _build_api(self):
        try:
            import logstash
        except ImportError:
            return None

        if not config.conf("LOGGING_LOGSTASH", False, cast=bool):
            return None

        return logstash.API()
