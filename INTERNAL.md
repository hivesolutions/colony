# Internal Distribution Information

## PyPI - the Python Package Index

In order to build colony for the PyPI run the following commands:

* `python setup.py process bdist_egg bdist_wininst upload`

In order to build it for source distribution use:

* `python setup.py process sdist upload`

TO build the "dumb" binary file use:

* `python setup.py process bdist upload`

Note that the account currently in use for colony is the joamag account.

For more information refer to [setuptools](http://packages.python.org/distribute/setuptools.html).

Please use the reference in the [setup()](http://docs.python.org/distutils/apiref.html) command for extended information.
