Configuration Storage
=====================

Cfgtree does not make any assumption of the way settings are stored, appart from the fact they are
all organized in a hierarchicla structure.

Some common storage format are provided out of the box by cfgtree, but developers can easily
implement their own configuration file format.

Single Json file
----------------

.. autoclass:: cfgtree.storages.JsonFileConfigStorage
    :members:
