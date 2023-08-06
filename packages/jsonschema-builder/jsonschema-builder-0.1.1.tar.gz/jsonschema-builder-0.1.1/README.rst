JSON Schema Builder
===================

Build `JSON schemas <http://json-schema.org>`_ easily in Python.

See documentation_ for more informations.

.. _documentation: https://jsonschema-builder.readthedocs.io

.. image:: https://img.shields.io/pypi/l/jsonschema-builder.svg?style=flat-square
   :target: https://pypi.python.org/pypi/jsonschema-builder/
   :alt: License

.. image:: https://img.shields.io/pypi/status/jsonschema-builder.svg?style=flat-square
   :target: https://pypi.python.org/pypi/jsonschema-builder/
   :alt: Development Status

.. image:: https://img.shields.io/pypi/v/jsonschema-builder.svg?style=flat-square
   :target: https://pypi.python.org/pypi/jsonschema-builder/
   :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/jsonschema-builder.svg?style=flat-square
   :target: https://pypi.python.org/pypi/jsonschema-builder/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/jsonschema-builder.svg?style=flat-square
   :target: https://pypi.python.org/pypi/jsonschema-builder/
   :alt: Supported Python implementations

.. image:: https://img.shields.io/pypi/wheel/jsonschema-builder.svg?style=flat-square
   :target: https://pypi.python.org/pypi/jsonschema-builder
   :alt: Download format

.. image:: https://travis-ci.org/link-society/jsonschema-builder.svg?branch=master&style=flat-square
   :target: https://travis-ci.org/link-society/jsonschema-builder
   :alt: Build status

.. image:: https://coveralls.io/repos/github/link-society/jsonschema-builder/badge.svg?style=flat-square
   :target: https://coveralls.io/r/link-society/jsonschema-builder
   :alt: Code test coverage

.. image:: https://landscape.io/github/link-society/jsonschema-builder/master/landscape.svg?style=flat-square
   :target: https://landscape.io/github/link-society/jsonschema-builder/master
   :alt: Code Health

Installation
------------

.. code-block:: text

   pip install jsonschema-builder

Usage
-----

.. code-block:: python

   import jsonschema
   import jsb

   schema = jsb.typed(
       jsb.schema(id='/schemas/myschema#', meta=jsb.draft04()),
       type='object',
       properties={
           'foo': jsb.typed(jsb.schema(), type='string'),
           'bar': jsb.typed(jsb.schema(), type='integer')
       }
   )
   data = {
       'foo': 'bar',
       'bar': 42
   }

   jsonschema.validate(data, schema)
