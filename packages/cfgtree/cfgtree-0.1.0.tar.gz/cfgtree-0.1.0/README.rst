===============================
cfgtree - Configuration as Tree
===============================

.. image:: https://travis-ci.org/Stibbons/cfgtree.svg?branch=master
    :target: https://travis-ci.org/Stibbons/cfgtree
.. image:: https://readthedocs.org/projects/cfgtree/badge/?version=latest
   :target: http://cfgtree.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/Stibbons/cfgtree/badge.svg
   :target: https://coveralls.io/github/Stibbons/cfgtree
.. image:: https://badge.fury.io/py/cfgtree.svg
   :target: https://pypi.python.org/pypi/cfgtree/
   :alt: Pypi package
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: ./LICENSE
   :alt: MIT licensed

* Free software: MIT
* Documentation: https://cfgtree.readthedocs.org/en/latest/
* Source: https://github.com/Stibbons/cfgtree

Description
===========

This module provides an easy yet comprehensive way of defining a configuration tree
for any application.

It requires the following acknolegdment:

- Application settings are organize in a hierarchical structure, dependend of the application
  itself. This structure is called in cfgtree: "bare config".

- User settings may come from different inputs:

  - environment variables (12 factors approach)
  - command line argument
  - configuration storage such as file (json, yaml, ini) or configuration server

Similar opensource projects
---------------------------

* Openstack's `Olso.config <https://docs.openstack.org/oslo.config/latest/>`_

Configuration Storage
---------------------

The trivial storage is a simple json file. The complete settings are placed inside it, such as::

    {
        'setting1': 'value1',
        'setting2': 'value2',
        'setting3': 'value3',
    }

But developer may want to organize in a more hierarchical structure, splitting into different files,
etc.

Another typical file format for configuration is YAML, which is more human readable and allow
inserting comments and so.

But, ultimately, all file format actually stores a hierarchical configuration.

Current Support:

- single Json file

Future support:

- Yaml file (with inplace save keeping comments and overall organization)
- Set of Yaml files
- Configuration server

Configuration Tree Description
------------------------------

Configuration hierarchy is to be described in a `cfgtree.EnvironmentConfig` inherited instance,
inside the member `.cfgtree`, using helper classes such as `StringCfg`, 'IntCfg', 'UserCfg' or
'PasswordCfg'. Each setting can be set by environment variable, command line parameter or by
the storage file(s) itself.

Let's take an example of an item defined at the first level of the hierarchy. It is defined as a
'IntCfg' with name 'count'. It can be set by the following:

- environment variable ``APPLICATIONNAME_COUNT`` (where ``APPLICATIONNAME`` is an optional
  developer-defined prefix added to every environment variable to avoid conflicts)
- command line argument ``--count``
- item `count` at the first level of a json file

Hierarchical structure is reflected in these different ways, to avoid conflicts. Now, the 'count'
setting is set in a settings section called 'general':

- environment variable: ``APPLICATIONNAME_GENERAL_COUNT``
- command line argument: ``--general-count``
- Json has a first level named ``general``, and inside one of the items is called ``count``.

XPath syntax
------------

A xpath-like syntax allows to reach any item of the configuration: ``<key1>.<key2>.<key3>.<item>``.

Documentation
=============

Full documentation is provided on `ReadTheDocs <https://cfgtree.readthedocs.org/en/latest/>`_.
