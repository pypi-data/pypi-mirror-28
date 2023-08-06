=====================================
cfgtree - App Configuration made easy
=====================================

.. image:: https://travis-ci.org/gsemet/cfgtree.svg?branch=master
    :target: https://travis-ci.org/gsemet/cfgtree
.. image:: https://readthedocs.org/projects/cfgtree/badge/?version=latest
   :target: http://cfgtree.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/gsemet/cfgtree/badge.svg
   :target: https://coveralls.io/github/gsemet/cfgtree
.. image:: https://badge.fury.io/py/cfgtree.svg
   :target: https://pypi.python.org/pypi/cfgtree/
   :alt: Pypi package
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: ./LICENSE
   :alt: MIT licensed

* Free software: MIT
* Documentation: https://cfgtree.readthedocs.org/en/latest/
* Source: https://github.com/gsemet/cfgtree

Description
===========

This package provides an easy yet comprehensive way of describing, storing and parsing a
user configuration.

It requires the following acknolegdments:

- Application settings actually represents a hierarchical structure, they can be organized into
  group of settings, subgroups, and they entierely depends on the application itself.

  This structure is called in cfgtree a "bare configuration", or "configuration tree".

- User settings may come from different inputs:

  - environment variables (12 factors approach). Example: ``MYAPP_VERBOSE``.
  - command line argument. Example: ``--verbose``
  - configuration storage such as file (json, yaml, ini) or configuration server. Example::

        {
            "verbose": true
        {

Similar opensource projects
---------------------------

* Openstack's `Olso.config <https://docs.openstack.org/oslo.config/latest/>`_

Overview
========

Please go to `ReadTheDocs <https://cfgtree.readthedocs.org/en/latest/>`_ for full, up-to-date
reference documentation.

Here is just a quick overview of cfgtree.

Configuration Tree Description
------------------------------

Configuration hierarchy is to be described in a ``cfgtree.EnvironmentConfig`` inherited instance,
inside the member ``.cfgtree``, using helper classes such as ``StringCfg``, ``IntCfg``, ``UserCfg``
or ``PasswordCfg``. Each setting can be set by environment variable, command line parameter or by
the storage file(s) itself.

Let's take an example of an item defined at the first level of the hierarchy. It is defined as a
``IntCfg`` with name ``count``. User can set this setting by:

- environment variable ``APPLICATIONNAME_COUNT`` (where ``APPLICATIONNAME`` is an optional,
  developer-defined prefix added to every environment variable of the application to avoid
  conflicts)
- command line argument ``--count``
- item `count` at the first level of a json file

Hierarchical structure is reflected in these different ways, to avoid conflicts. Now, let's imagine
the 'count' setting is set in a group called 'general':

- environment variable is: ``APPLICATIONNAME_GENERAL_COUNT``
- command line argument is: ``--general-count``
- Json has a first level named ``general``, and inside one of the items is called ``count``::

    {
        "general": {
            "count": 1
        }
    }

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

cfgtree allows complete customization of the file storage, developers can even develop their own.

Another typical file format for configuration is YAML, which is more human readable and allow
inserting comments and so. INI files is often found as configuration format, or TOML.

But, ultimately, all file formats actually store settings in hierarchical configuration.

Current Support:

- single Json file

Future support:

- Yaml file (with inplace save keeping comments and overall organization)
- Set of Yaml files
- Configuration server

Access to settings
------------------

In your application, an xpath-like syntax allows you to reach any item of the configuration:
``<key1>.<key2>.<key3>.<item>``. See the documentation for full explanation.

Documentation
=============

Full documentation is provided on `ReadTheDocs <https://cfgtree.readthedocs.org/en/latest/>`_.



