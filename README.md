# [![Colony Framework](res/logo.png)](http://getcolony.com)

The Colony Framework is an open-source plugin framework specification. Its implementations provide a component model at runtime, enabling plugins to be installed, started, stopped, updated, and uninstalled without having to stop the application container. The framework heavily relies on the Inversion of Control principle, making it easier for application components to discover and interact with each other.

Colony's goal is to simplify the process of creating modular applications by offering a unified, simplified model for component development. This can have practical applications in a variety of fields, ranging from modular enterprise software to application mashing.

## Quick start

### Handicraft

* Install Colony using `pip install colony`
* Run the command `RUN_MODE=devel colony`

### [Virtualenv](https://virtualenv.pypa.io/)

* Start and activate the environment using `virtualenv .venv && source .venv/bin/activate`
* Install Colony in the system using `pip install colony`
* Deploy the console package using `cpm install console_interface`
* Run your new colony using the command `RUN_MODE=devel colony`

### Docker

* Create a new directory to serve as the base for the build `mkdir colony && cd colony`
* Retrieve the `Dockerfile` from the repo using `wget https://github.com/hivesolutions/colony/raw/master/assets/docker/Dockerfile`
* Create the new docker image using `docker build --tag self/colony .`
* Execute colony with `docker run -e RUN_MODE=devel -i -t self/colony`

To actually do something useful, look into [How to Establish your Colony in 3 Easy Steps](http://getcolony.com/docs/colony/documentation_how_to_establish_your_colony_in_3_easy_steps.html)

## Installation

### For development

* Set `PYTHONPATH` to the `colony/src` path so that the Python source files may be included
* Set `PATH` to the `colony/scripts/pypi` to use the provided base scripts

### For production

* Installation via pip: `pip install colony`

## Configuration

| Name                 | Type   | Default       | Description                                                                           |
| -------------------- | ------ | ------------- | ------------------------------------------------------------------------------------- |
| **RUN_MODE**         | `str`  | `development` | The mode in which the Colony will be running.                                         |
| **LOGGING_LOGSTASH** | `bool` | `False`       | If the [Logstash](https://www.elastic.co/logstash) logging adapter should be enabled. |

## Usage

Most of the colony operations are run through the `cpm` command:

* `cpm clone <target>` - clones the base colony instance into the target directory (new project)
* `cpm cleanup <target>` - cleans the current instance, removing extra files
* `cpm pack <target>` - packs the current instance into a .zip file
* `cpm generate [target] <...>` - generates a .json descriptor file for the provided Python file and then runs
the build operation for the generated .json file, effectively building the package item
* `cpm build [descriptor] <...>` - builds the target .json descriptor file into a package file
* `cpm deploy [package]` - deploys the target .cbx file into the current instance
* `cpm info [package]` - prints information about the package to the standard output
* `cpm install [name] <...>` - installs the package with the provided name from the remote repositories
* `cpm upgrade` - updates the complete set of packages deployed in the instance
* `cpm require [path] <...>` - installs the complete set of packages defined in the requirements file
* `cpm upload [target] <repo>` - generates a package for the provided path and then uploads it to the currently
configured primary repository or another repository if defined

## Testing

To run the complete set of available tests for the deployment, use either `colony test`
or `MODE=test colony` and Colony Manager will boot directly to unit testing and exit in error in
case at least one test fails.

## Features

* Runtime modularity.
* No restart is required for deploying new plugins or updating or reconfiguring existing ones.
* Simplified component model (easy to create a plugin, even easier to combine existing ones).
* Capabilities: simple extension points that allow your plugins to take advantage of future plugins that adhere to the capability API.
* Dependencies: simplified dependency management, declare the id of the plugin your plugin needs to function, and the plugin manager
will ensure your plugin only gets loaded when the conditions are met.
* Most importantly, runs [Colony Plugins](https://github.com/hivesolutions/colony_plugins).

And remember, this is just the base runtime. To understand what you can do with Colony,
browse the [Colony Plugins repository](https://github.com/hivesolutions/colony_plugins).

## Contributing

Although Colony is still in an early stage, we're welcoming help for all kinds of work.
The best ways to get involved:

1. Join the [mailing list](http://groups.google.com/group/colony-users).
2. Send pull requests for bug fixes or new features and improvements.
3. Help make the [docs](http://getcolony.com/docs/colony/) better.

## Extensions

To find the Python native extension required for some of the plugins, use the following sites:

* Python Imaging Library (PIL) [link](https://pillow.readthedocs.io/).
* Reportlab PDF Generator [link](http://www.reportlab.com/).
* Unofficial Windows Binaries for Python Extension Packages [link](http://www.lfd.uci.edu/~gohlke/pythonlibs/).
* MySQL driver for Python [link](http://sourceforge.net/projects/mysql-python/).

## Project information

* Colony Base Source: https://github.com/hivesolutions/colony
* Colony Base Plugins Source: https://github.com/hivesolutions/colony_plugins
* Web: http://getcolony.com
* Docs: http://getcolony.com/docs/colony/
* Mailing list: http://groups.google.com/group/colony-users
* Twitter: http://twitter.com/colonyframework

## License

Colony is an open-source project currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://app.travis-ci.com/hivesolutions/colony.svg?branch=master)](https://travis-ci.com/github/hivesolutions/colony)
[![Build Status GitHub](https://github.com/hivesolutions/colony/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/colony/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/colony/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/colony?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/colony.svg)](https://pypi.python.org/pypi/colony)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
