.. cfgtree documentation master file, created by
   sphinx-quickstart on Sat Jan  6 10:37:36 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Cfgtree Documentation
================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    overview
    reference/cfgtree
    reference/storages
    release_notes

Introduction
------------

``cfgtree`` provides an easy yet comprehensive way of describing, storing and parsing a
user configuration for you Python application.

It requires the following acknolegdments:

- Application settings actually represents a hierarchical structure, they can be organized into
  group of settings, subgroups, and they entierely depends on the application itself.

  This structure is called in Cfgtree a "bare configuration", or "configuration tree".

- User settings may come from different inputs:

  - environment variables (12 factors approach). Example: ``MYAPP_VERBOSE=1``.
  - command line argument. Example: ``--verbose``
  - configuration storage such as file (JSON, YAML, INI) or even configuration server. Example:

    .. code-block:: javascript

        {
            "verbose": true
        {

This allows you to define once your settings structure, and let the user of your application define
the settings throught different ways. For instance, your application can read some settings through
command line arguments, which is very useful for containerization of your application. It is indeed
recommended by `Heroku's 12 Factor Good Practices <https://12factor.net/fr/config>`_.

Describing your configuration through a model also allows to have a configuration validator without
having to maintain both a file schema (ex: JSON Schema) and the parsing logic code.

Similar opensource projects
---------------------------

* Openstack's `Olso.config <https://docs.openstack.org/oslo.config/latest/>`_
