Getting Started
===============

Defining a database schema with PyDAL
-------------------------------------

.. code-block:: python

   from schemapy import DAL, Field
   

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

Using validators
----------------

Default validators are found in the ``schemapy.validators`` module.

Example:

.. code-block:: python

   def IS_OF(cls):
       def validator(value):
           if not isinstance(value, cls):
               return (value, 'wrong type')

           else:
               return (value, None)

       return validator


   db.define_table(
       'persons',
       Field('name', type='string', requires=[IS_OF(str)], required=True),
       Field('age', type='integer', requires[IS_OF(int)], required=True)
   )

Creating an API from a database
-------------------------------

.. code-block:: python

   from schemapy import API


   api = API(db)

*CRUD* methods are automatically created:

.. code-block:: python

   print(api.select_all_persons())
   print(api.create_persons(name='john', age=12))
   print(api.create_persons(name='bob', age='wrong'))  # will raise an error
   print(api.update_persons(id=1, name='john smith'))
   print(api.delete_persons(id=1))

Creating a custom API
---------------------

.. code-block:: python

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

Usage:

.. code-block:: python

   now = datetime.now()
   result = api.select_posts_by_date(
       begin=now - timedelta(days=1),
       end=now
   )
   print(list(result))
