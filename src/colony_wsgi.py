#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
WSGI Adapter for Hive Colony Framework

This module provides a WSGI (Web Server Gateway Interface) compliant adapter
that allows the Hive Colony plugin-based framework to be deployed behind any
WSGI-compatible web server (e.g., Gunicorn, uWSGI, mod_wsgi, etc.).

The primary purpose of this module is to bridge the Colony plugin system with
standard Python web server infrastructure. It initializes the Colony plugin
manager and exposes a WSGI `application` callable that delegates HTTP request
handling to the Colony WSGI plugin.

Basic standalone usage::

    $ python -m colony_wsgi

With Gunicorn (4 workers)::

    $ gunicorn colony_wsgi:application -w 4 --bind 0.0.0.0:8080

With uWSGI::

    $ uwsgi --http :8080 -w colony_wsgi:application

With Uvicorn::

    $ uvicorn colony_wsgi:application --host 0.0.0.0 --port 8080 --interface wsgi

Development with auto-reload::

    $ SERVER=legacy HOST=127.0.0.1 PORT=8080 python -m colony_wsgi

Production with SSL::

    $ SERVER=netius SSL=true KEY_FILE=server.key CER_FILE=server.crt python -m colony_wsgi
"""

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
import sys
import time
import atexit
import signal
import traceback
import threading

CONFIG_FILE_ENV = "COLONY_CONFIG_FILE"
""" The name of the environment variable to be used
to retrieve the path to the configuration file """

DEFAULT_CONFIG_PATH = "config/python/devel.py"
""" The path to the default configuration file to be
used in case no path is specified using the environment
variable bases strategy """

EXCLUDED_NAMES = ("server", "host", "port", "ssl", "key_file", "cer_file")
""" The sequence that contains the names that are considered
excluded from the auto parsing of parameters """

# retrieves the base path for the current file and uses
# it to insert it in the current system path in case it's
# not already present (required for module importing)
base_path = os.path.dirname(__file__)
if not base_path in sys.path:
    sys.path.insert(0, base_path)

import colony

# tries to retrieve the prefix to be used to shorten the path
# resolution in the request handling
prefix = colony.conf("PREFIX", None)
prefix = colony.conf("COLONY_PREFIX", prefix)

# gathers the path to the alias file that contains JSON information
# about the mapping prefixes for the HTTP server, the file should
# contain a set of prefix to resolution prefix values
alias_path = colony.conf("ALIAS_PATH", None)
alias_path = alias_path and os.path.expanduser(alias_path)
alias_path = alias_path and os.path.normpath(alias_path)

# gathers the path to the rewrite file that contains JSON information
# about the rewrite meta information to be used at runtime to shorten
# the provided URL path values (useful under proxy redirection)
rewrite_path = colony.conf("REWRITE_PATH", None)
rewrite_path = rewrite_path and os.path.expanduser(rewrite_path)
rewrite_path = rewrite_path and os.path.normpath(rewrite_path)

# creates the plugin manager instance with the current file path
# as the manager path and the corresponding relative log path,
# then provides the plugin and meta paths and unsets the global
# loop strategy (avoids blocking the process), note also that
# threads are disallowed to avoid creation of extra threads, the
# signal handlers are disabled to avoid collisions
plugin_manager, return_code = colony.PluginManager.build(
    loop=False,
    threads=False,
    signals=False,
    container="wsgi",
    base_path=base_path,
)
alias = None
rewrite = None


def application(environ, start_response):
    try:
        # retrieves the currently set alias and rewrite lists,
        # loading them it in case this is the first run, these
        # value may be unset and no mapping is performed under
        # such situations (applicable for both alias and rewriting)
        alias = get_alias()
        rewrite = get_rewrite()

        # retrieves the wsgi plugin and uses it to handle
        # the wsgi request (request redirection) any inner
        # exception should be handled and an error HTTP
        # message should be returned to the end user
        wsgi_plugin = plugin_manager.get_plugin("pt.hive.colony.plugins.wsgi")
        if not wsgi_plugin:
            raise colony.PluginSystemException("no WSGI plugin found")
        if not wsgi_plugin.is_loaded():
            raise colony.PluginSystemException("WSGI plugin not loaded")
        sequence = wsgi_plugin.handle(environ, start_response, prefix, alias, rewrite)
    except Exception:
        # in case the run mode is development the exception should
        # be processed and a description sent to the output
        if plugin_manager.run_mode == "development":
            # prints a description of the exception and then
            # sends the traceback of it to the output
            traceback.print_exc(file=sys.stdout)

        # raises the exception back to the stack to be handled
        # by the upper levels
        raise

    # returns the sequence object that may be used by the caller
    # method to retrieve the contents of the message to be sent
    return sequence


def get_alias(encoding="utf-8"):
    global alias
    global alias_path

    # in case either the alias is defined (file already loaded)
    # or there's no alias file to be loaded the currently set
    # alias variable is retrieved (cached value)
    if alias or not alias_path:
        return alias

    try:
        # tries to load the JSON file using the default python
        # based JSON module (may not exist) the closes the file
        # to avoid any memory reference leak
        import json

        file = open(alias_path, "rb")
        try:
            data = file.read()
        finally:
            file.close()
        data = data.decode(encoding)
        alias = json.loads(data)
    except Exception:
        # unsets the alias path to avoid any further file reading
        # avoiding any duplicated reading
        alias_path = None

    # returns the map containing the alias that were loaded from the
    # file, this value may be unsets in case there was an error
    return alias


def get_rewrite(encoding="utf-8"):
    global rewrite
    global rewrite_path

    # in case either the rewrite is defined (file already loaded)
    # or there's no rewrite file to be loaded the currently set
    # rewrite variable is retrieved (cached value)
    if rewrite or not rewrite_path:
        return rewrite

    try:
        # tries to load the JSON file using the default python
        # based JSON module (may not exist) the closes the file
        # to avoid any memory reference leak
        import json

        file = open(rewrite_path, "rb")
        try:
            data = file.read()
        finally:
            file.close()
        data = data.decode(encoding)
        rewrite = json.loads(data)
    except Exception:
        # unsets the rewrite path to avoid any further file reading
        # avoiding any duplicated reading
        rewrite_path = None

    # returns the map containing the rewrite that were loaded from the
    # file, this value may be unsets in case there was an error
    return rewrite


@atexit.register
def unload_system():
    # registers a dummy signal handler for the SIGINT and SIGTERM signals
    # so that no actions are performed on the signals (avoids duplicate
    # signal issues), this prevents a user from sending multiple requests
    # to unload the system (eg: multiple CTRL + C presses)
    signal.signal(signal.SIGINT, lambda _s, _f: ())
    signal.signal(signal.SIGTERM, lambda _s, _f: ())

    # unloads the plugin manager system releasing all
    # the used resources and killing all the threads
    # this should be enough to return the control to
    # the embedding process
    plugin_manager.unload_system(kill_timer=False)


class ServerThread(threading.Thread):
    """
    Thread class responsible for the handling and management
    of the server instance that it represents.

    This is considered to be a long running thread and only
    the exit of the current process "kills" it.
    """

    def __init__(
        self,
        server="netius",
        host="127.0.0.1",
        port=8080,
        ssl=False,
        key_file=None,
        cer_file=None,
        kwargs=dict(),
        *args,
        **_kwargs
    ):
        threading.Thread.__init__(self, *args, **_kwargs)
        self.server = server
        self.host = host
        self.port = port
        self.ssl = ssl
        self.key_file = key_file
        self.cer_file = cer_file
        self.kwargs = kwargs
        self.daemon = True

    def __repr__(self):
        return "%s / %s@%d" % (self.server, self.host, self.port)

    def run(self):
        try:
            serve(
                server=self.server,
                host=self.host,
                port=self.port,
                ssl=self.ssl,
                key_file=self.key_file,
                cer_file=self.cer_file,
                kwargs=self.kwargs,
            )
        except Exception:
            sys.stderr.write("Problem in '%s'" % str(self) + "\n")
            raise


def serve_multiple(
    server="netius",
    hosts=("127.0.0.1",),
    ports=(8080,),
    ssl=False,
    key_file=None,
    cer_file=None,
    kwargs=dict(),
):
    threads = []
    count = len(hosts)

    for index in range(count):
        host = hosts[index]
        port = ports[index]

        thread = ServerThread(
            server=server,
            host=host,
            port=port,
            ssl=ssl,
            key_file=key_file,
            cer_file=cer_file,
            kwargs=kwargs,
        )
        thread.start()
        threads.append(thread)

    return threads


def serve(
    server="netius",
    host="127.0.0.1",
    port=8080,
    ssl=False,
    key_file=None,
    cer_file=None,
    kwargs=dict(),
):
    _globals = globals()

    method = _globals.get("serve_" + server, serve_legacy)
    version_method = _globals.get("version_" + server, None)
    server_version = version_method() if version_method else None
    if server_version:
        sys.stderr.write(
            "Starting Colony WSGI with '%s' version '%s' ..." % (server, server_version)
            + "\n"
        )
    else:
        sys.stderr.write("Starting Colony WSGI with '%s' ..." % server + "\n")
    return_value = method(
        host=host, port=port, ssl=ssl, key_file=key_file, cer_file=cer_file, **kwargs
    )
    sys.stderr.write("Stopped Colony WSGI using '%s' ..." % server + "\n")
    return return_value


def serve_waitress(host, port, **kwargs):
    import waitress

    waitress.serve(application, host=host, port=port)


def serve_netius(host, port, ssl=False, key_file=None, cer_file=None, **kwargs):
    import netius.servers

    server = netius.servers.WSGIServer(application, **kwargs)
    server.serve(host=host, port=port, ssl=ssl, key_file=key_file, cer_file=cer_file)


def serve_tornado(host, port, ssl=False, key_file=None, cer_file=None, **kwargs):
    import tornado.wsgi
    import tornado.httpserver

    ssl_options = ssl and dict(keyfile=key_file, certfile=cer_file) or None

    container = tornado.wsgi.WSGIContainer(application)
    server = tornado.httpserver.HTTPServer(container, ssl_options=ssl_options)
    server.listen(port, address=host)
    instance = tornado.ioloop.IOLoop.instance()
    instance.start()


def serve_cherry(host, port, **kwargs):
    import cherrypy.wsgiserver

    server = cherrypy.wsgiserver.CherryPyWSGIServer((host, port), application)
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        server.stop()


def serve_legacy(host, port, **kwargs):
    import wsgiref.simple_server

    httpd = wsgiref.simple_server.make_server(host, port, application)
    sys.stderr.write("Running on http://%s:%d/" % (host, port) + "\n")
    httpd.serve_forever()


def version_netius():
    import netius

    return netius.VERSION


def main():
    kwargs = dict()
    server = colony.conf("SERVER", "legacy")
    host = colony.conf("HOST", "127.0.0.1")
    port = colony.conf("PORT", "8080")
    base_port = colony.conf("BASE_PORT", None, cast=int)
    number_threads = colony.conf("NUMBER_THREADS", None, cast=int)
    ssl = colony.conf("SSL", False, cast=bool)
    key_file = colony.conf("KEY_FILE", None)
    cer_file = colony.conf("CER_FILE", None)
    for name, value in os.environ.items():
        if not name.startswith("SERVER_"):
            continue
        name_s = name.lower()[7:]
        if name_s in EXCLUDED_NAMES:
            continue
        kwargs[name_s] = value

    host = str(host)
    port = str(port)

    hosts = [value.strip() for value in host.split(",")]
    ports = [int(value.strip()) for value in port.split(",")]

    # in case a base port and number of threads are defined
    # then the ports are calculated by adding the base port
    # to the index for the number of threads
    if base_port and number_threads:
        ports = [base_port + index for index in range(number_threads)]
        end_port = ports[-1]
    else:
        end_port = None

    # in case there's only one host defined but multiple ports
    # are defined (more than one server instance is required)
    # then the host is duplicated for the number of ports
    if len(hosts) == 1 and len(ports) > 1:
        hosts = hosts * len(ports)

    _globals = globals()
    version_method = _globals.get("version_" + server, None)
    server_version = version_method() if version_method else None

    plugin_manager.set_exec_param("server", server)
    plugin_manager.set_exec_param("hosts", hosts)
    plugin_manager.set_exec_param("ports", ports)
    plugin_manager.set_exec_param("base_port", base_port)
    plugin_manager.set_exec_param("end_port", end_port)
    plugin_manager.set_exec_param("number_threads", number_threads)
    plugin_manager.set_exec_param("ssl", ssl)
    plugin_manager.set_exec_param("key_file", key_file)
    plugin_manager.set_exec_param("cer_file", cer_file)
    plugin_manager.set_exec_param("kwargs", kwargs)
    plugin_manager.set_exec_param("thread_count", len(hosts))
    plugin_manager.set_exec_param("server_version", server_version)

    serve_multiple(
        server=server,
        hosts=hosts,
        ports=ports,
        ssl=ssl,
        key_file=key_file,
        cer_file=cer_file,
        kwargs=kwargs,
    )

    def handler(signum=None, frame=None):
        raise SystemExit()

    signal.signal(signal.SIGTERM, handler)

    run = True
    while run:
        try:
            time.sleep(86400)
        except (KeyboardInterrupt, SystemExit):
            run = False


if __name__ == "__main__":
    main()
else:
    __path__ = []
