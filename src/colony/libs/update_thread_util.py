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

import time
import threading

class UpdateThread(threading.Thread):
    """
    The update thread class.
    """

    stop_flag = False
    """ The stop flag """

    timeout = None
    """ The timeout between calls """

    call_method = None
    """ The method to be called """

    call_arguments = []
    """ The call arguments """

    def __init__(self):
        """
        Constructor of the class.
        """

        threading.Thread(self)

        self.daemon = True

    def stop(self):
        """
        Stops the update thread.
        """

        self.stop_flag = True

    def get_timeout(self):
        """
        Retrieves the timeout value.

        :rtype: int
        :return: The timeout value.
        """

        return self.timeout

    def set_timeout(self, timeout):
        """
        Sets the timeout value.

        :type timeout: int
        :param timeout: The timeout value.
        """

        self.timeout = timeout

    def get_call_method(self):
        """
        Retrieves the call method.

        :rtype: Method
        :return: The call method.
        """

        return self.call_method

    def set_call_method(self, call_method):
        """
        Sets the call method.

        :type call_method: Method
        :param call_method: The call method.
        """

        self.call_method = call_method

    def get_call_arguments(self):
        """
        Retrieves the call arguments.

        :rtype: List
        :return: The call arguments.
        """

        return self.call_arguments

    def set_call_arguments(self, call_arguments):
        """
        Sets the call arguments.

        :type call_arguments: List
        :param call_arguments: The call argument.
        """

        self.call_arguments = call_arguments

    def run(self):
        # unsets the stop flag
        self.stop_flag = False

        # while the thread is valid
        while not self.stop_flag:
            # sleep for the given timeout time
            time.sleep(self.timeout)

            # in case the stop flag is set
            if self.stop_flag:
                # breaks the cycle
                break

            # calls the method
            self.call_method(*self.call_arguments)
