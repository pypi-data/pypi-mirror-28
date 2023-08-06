Advanced usage
==============

Using with SQLAlchemy
---------------------

Firstly, create a schema:

.. code-block:: python

   from sqlalchemy import create_engine, Column, Integer, String
   from sqlalchemy.orm import sessionmaker
   from sqlalchemy.ext.declarative import declarative_base


   engine = create_engine('sqlite://:memory:')
   Base = declarative_base()


   class Person(Base):
       id = Column(Integer, primary_key=True)
       name = Column(String(255))


   Base.metadata.create_all(engine)
   DBSession = sessionmaker(bind=engine)
   session = DBSession()

Then:

.. code-block:: python

   from schemapy import API, Field


   # disable actions generation from PyDAL (you can feed your own generator)
   api = API(db, schema_actions_generator=None)


   @api.as_action(
       type='read',
       request=[Field('name', type='string', required=True)],
       response=[
           Field('id', type='integer'),
           Field('name', type='string')
       ]
   )
   def select_persons_by_name(db, req, action):
       return [
           {'id': person.id, 'name': person.name}
           for person in db.query(Person).filter(Person.name == req.name).all()
       ]
