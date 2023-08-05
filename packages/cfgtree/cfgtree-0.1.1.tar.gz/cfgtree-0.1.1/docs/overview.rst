
Overview
========

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
- Json has a first level named ``general``, and inside one of the items is called ``count``:

  .. code-block:: javascript

      {
          "general": {
              "count": 1
          }
      }

Configuration Storage
---------------------

The trivial storage is a simple json file. The complete settings are placed inside it, such as:

.. code-block:: javascript

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
