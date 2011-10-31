# [Colony Framework](http://getcolony.com)
The Colony Framework is an open source plugin framework specification. Implementations of the specification offer a runtime component model, that allows for plugins to be installed, started, stopped, updated and uninstalled without requiring the application container to be stopped. The specification relies heavily on the Inversion of control principle, in order to make it easier for application components to discover and interact with each other.

Colony aims to eliminate the complexity typically associated with the creation of modular applications, through a simplified unified model for component development. Practical applications can range from modular enterprise software to application mashing.

## Quick start

* Download [Colony](http://hivesolutions.dyndns.org/integration_public/LATEST_SUCCESS/resources/colony_1.0.0_all.zip).
* Unzip the file, which will create a colony directory.
* Go to colony/scripts/<platform>.
* Run the command 'colony'

To actually do something useful look into [How to Establish your Colony in 3 Easy Steps](http://getcolony.com/docs/colony/documentation_how_to_establish_your_colony_in_3_easy_steps.html)

## Features

* Runtime modularity.
* No restart required for deploying new plugins, updating or reconfiguring existing ones.
* Simplified component model (easy to create a plugin, even easier to combine existing ones).
* Capabilities: simple extension points which allow your plugins to take advantage of future plugins which adhere to the capability API.
* Dependencies: simplified dependency management, just declare the id of the plugin your plugin needs in order to function and the plugin manager will ensure your plugin only gets loaded when the conditions are met.
* Most importantly, runs [Colony Plugins](https://github.com/hivesolutions/colony_plugins).

And remember this is just the base runtime, to understand the kind of things you can do with Colony, browse the [Colony Plugins repository](https://github.com/hivesolutions/colony_plugins).

## Contributing

Altough Colony is still in an early stage we're welcoming help for all kinds of work.
The best ways to get involved:

1. Join the [mailing list](http://groups.google.com/group/colony-users).
2. Send pull requests for bug fixes or new features and improvements.
3. Help make the [docs](http://getcolony.com/docs/colony/) better.

## Project information

* Colony Base Source: https://github.com/hivesolutions/colony
* Colony Base Plugins Source: https://github.com/hivesolutions/colony_plugins
* Web: http://getcolony.com
* Docs: http://getcolony.com/docs/colony/
* Mailing list: http://groups.google.com/group/colony-users
* Twitter: http://twitter.com/colonyframework

## License

Colony is an open-source project licensed under the [GNU General Public License Version 3](http://www.gnu.org/licenses/gpl.html).
