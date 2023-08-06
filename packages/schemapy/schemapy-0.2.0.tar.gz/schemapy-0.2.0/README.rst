Schemapy
========

*Schemapy* allows you to generate objects for centralized database access. You
define the schema for your API, the code that needs to be executed, then the
validation part is dealt with for you. Everything is then encapsulated in a single
object.

*Schemapy* relies on PyDAL_ for schema definition but is not tied to it.

See documentation_ for more informations.

.. _documentation: https://schemapy.readthedocs.io
.. _PyDAL: https://github.com/web2py/pydal

.. image:: https://img.shields.io/pypi/l/schemapy.svg?style=flat-square
   :target: https://pypi.python.org/pypi/schemapy/
   :alt: License

.. image:: https://img.shields.io/pypi/status/schemapy.svg?style=flat-square
   :target: https://pypi.python.org/pypi/schemapy/
   :alt: Development Status

.. image:: https://img.shields.io/pypi/v/schemapy.svg?style=flat-square
   :target: https://pypi.python.org/pypi/schemapy/
   :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/schemapy.svg?style=flat-square
   :target: https://pypi.python.org/pypi/schemapy/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/schemapy.svg?style=flat-square
   :target: https://pypi.python.org/pypi/schemapy/
   :alt: Supported Python implementations

.. image:: https://img.shields.io/pypi/wheel/schemapy.svg?style=flat-square
   :target: https://pypi.python.org/pypi/schemapy
   :alt: Download format

.. image:: https://travis-ci.org/linkdd/schemapy.svg?branch=master&style=flat-square
   :target: https://travis-ci.org/linkdd/schemapy
   :alt: Build status

.. image:: https://coveralls.io/repos/github/linkdd/schemapy/badge.svg?style=flat-square
   :target: https://coveralls.io/r/linkdd/schemapy
   :alt: Code test coverage

.. image:: https://landscape.io/github/linkdd/schemapy/master/landscape.svg?style=flat-square
   :target: https://landscape.io/github/linkdd/schemapy/master
   :alt: Code Health

Installation
------------

.. code-block:: text

   pip install schemapy

Usage
-----

Using *PyDAL*:

.. code-block:: python

   from schemapy import API, DAL, Field
   from datetime import datetime, timedelta
   
   db = DAL('sqlite:memory')
   db.define_table(
       'users',
       Field('name', type='string', required=True),
       Field('created_on', type='date')
   )
   
   db.define_table(
       'posts',
       Field('subject', type='string', required=True),
       Field('author', type='reference users', required=True),
       Field('created_on', type='date'),
       Field('content', type='text', required=True)
   )
   
   api = API(db)
   
   @api.as_action(
       type='read',
       request=[
           Field('begin', type='date', required=True),
           Field('end', type='date', required=True)
       ],
       response=db.posts
   )
   def select_posts_by_date(db, req, action):
       query = (db.posts.created_on >= req.begin) | (db.posts.created_on <= req.end)
       return db(query).select()
   
   now = datetime.now()
   result = api.select_posts_by_date(
       begin=now - timedelta(days=1),
       end=now
   )
   print(list(result))
