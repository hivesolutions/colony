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

import os
import signal
import subprocess

WINDOWS_KILL_COMMAND = "taskkill /F /T /PID %i"
""" The windows kill command """

NT_PLATFORM_VALUE = "nt"
""" The nt platform value """

DOS_PLATFORM_VALUE = "dos"
""" The dos platform value """

WINDOWS_PLATFORMS_VALUE = (
    NT_PLATFORM_VALUE,
    DOS_PLATFORM_VALUE
)
""" The windows platform value """

def kill_process(pid, signal = None):
    """
    Kills the process with the given pid (process identifier)
    and "using" the given signal.

    :type pid: int
    :param pid: The identifier of the process to be killed.
    :type signal: signal
    :param signal: The signal to be used to kill the process.
    """

    # retrieves the current os name
    os_name = os.name

    # in case the current operative system is windows based
    if os_name in WINDOWS_PLATFORMS_VALUE:
        # kills the process using windows methods
        _kill_process_windows(pid)
    # otherwise it must be a unix platform
    else:
        # kills the process using unix methods
        _kill_process_unix(pid)

def _kill_process_windows(pid):
    """
    Kills the process with the given pid (process identifier).
    This class focus in the strategy used in windows operative
    systems.

    :type pid: int
    :param pid: The identifier of the process to be killed.
    """

    # in case the os module contains the kill method
    if hasattr(os, "kill"):
        # kills the process with the given pid
        os.kill(pid, signal.SIGTERM)
    else:
        # crates a process to kill the process with the given pid
        subprocess.Popen(WINDOWS_KILL_COMMAND % pid, shell = True)

def _kill_process_unix(pid, _signal = None):
    """
    Kills the process with the given pid (process identifier).
    This class focus in the strategy used in unix platforms.

    :type pid: int
    :param pid: The identifier of the process to be killed.
    """

    # sets the signal value
    _signal = _signal or signal.SIGKILL #@UndefinedVariable

    # kills the process with the given pid
    # and with the given signal
    os.kill(pid, _signal) #@UndefinedVariable
