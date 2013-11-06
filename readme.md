# [Colony Framework](http://getcolony.com)
The Colony Framework is an open source plugin framework specification. Implementations of the specification offer a runtime component model, that allows for plugins to be installed, started, stopped, updated and uninstalled without requiring the application container to be stopped. The specification relies heavily on the Inversion of control principle, in order to make it easier for application components to discover and interact with each other.

Colony aims to eliminate the complexity typically associated with the creation of modular applications, through a simplified unified model for component development. Practical applications can range from modular enterprise software to application mashing.

## Quick start

* Download [Colony](http://hivesolutions.dyndns.org/integration_public/LATEST_SUCCESS/resources/colony_1.0.0_all.zip).
* Unzip the file, which will create a colony directory.
* Go to colony/scripts/<platform>.
* Run the command 'colony'

To actually do something useful look into [How to Establish your Colony in 3 Easy Steps](http://getcolony.com/docs/colony/documentation_how_to_establish_your_colony_in_3_easy_steps.html)

## Installation

### For development

* Set `PYTHONPATH` to the `colony/src` path so that the python source files may be included
* Set `PATH` to the `colony/scripts/pypi` to used the provided base scripts

### For production

## Usage

Most of the colony operation are run through the `colony_admin` command:

* `colony_admin clone <target>` - clones the base colony instance into the target directory (new project)
* `colony_admin cleanup <target>` - cleans the current instance removing extra files
* `colony_admin pack <target>` - packs the current instance into a zip file
* `colony_admin build [target]` - builds the target descriptor file into a cbx file
* `colony_admin deploy [target]` - deploys the target cbx file into the current instance

## Features

* Runtime modularity.
* No restart required for deploying new plugins, updating or reconfiguring existing ones.
* Simplified component model (easy to create a plugin, even easier to combine existing ones).
* Capabilities: simple extension points which allow your plugins to take advantage of future plugins which adhere to the capability API.
* Dependencies: simplified dependency management, just declare the id of the plugin your plugin needs in order to function and the plugin manager will ensure your plugin only gets loaded when the conditions are met.
* Most importantly, runs [Colony Plugins](https://github.com/hivesolutions/colony_plugins).

And remember this is just the base runtime, to understand the kind of things you can do with Colony, browse the [Colony Plugins repository](https://github.com/hivesolutions/colony_plugins).

## Contributing

Although Colony is still in an early stage we're welcoming help for all kinds of work.
The best ways to get involved:

1. Join the [mailing list](http://groups.google.com/group/colony-users).
2. Send pull requests for bug fixes or new features and improvements.
3. Help make the [docs](http://getcolony.com/docs/colony/) better.

## Extensions

To find python native extension required for some of the plugins used the following sites:

* Python Imaging Library (PIL) [link](http://www.pythonware.com/products/pil/).
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

Colony is an open-source project licensed under the [GNU General Public License Version 3](http://www.gnu.org/licenses/gpl.html).
