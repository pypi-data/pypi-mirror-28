Pony Database Facade
====================

|PyPI| |LICENCE| |STARS|

PonyORM Database object Facade. The package encapsulates the names of the parameters used in the low-level modules.

`Русская документация`_


Installation
------------

::

  pip install pony-database-facade


Constructor
-----------

The ``DatabaseFacade`` constructor and the ``bind`` method takes the following arguments:

provider
  The name of the database provider.
  One of the list: ``sqlite``, ``mysql``, ``postgres`` or ``oracle``.
  By default is ``sqlite``.

dbname
  The name of the database.
  If you are using SQLite, the name of the file in which SQLite will store the data and by default is ``:memory:``.

host
  Name of host to connect to.
  By default is ``localhost``.

port
  TCP port of database server.
  By default is standard port.

user
  User to authenticate as.
  By default is ``None``.

password
  Password to authenticate with.
  By default is ``None``.

charset (MySQL only)
  By default is ``utf8``.

create_db (SQLite only)
  Try to create the database if such filename doesn’t exists.
  By default is ``True``.

\*args
  parameters required by the database driver.

\*\*kwargs
  parameters required by the database driver.

.. code:: python

    # SQLite in memory
    db = DatabaseFacade()

    # MySQL, localhost, no user, no password, used database blog
    db = DatabaseFacade('mysql', dbname='blog')
    db = DatabaseFacade(provider='mysql', dbname='blog')

    # PostgreSQL
    db = DatabaseFacade()
    db.bind('postgres',
            host='my.vps.com',
            user='anyone',
            password='anykey',
            dbname='blog')


Connection
----------

To connect to the database, use the ``connect`` method.
This method takes the same arguments as `generate_mapping`_, but the default for ``create_tables`` is ``True``.
This method also calls the ``bind`` method.

.. code:: python

    db = DatabaseFacade()
    db.connect()


Full example
------------

.. code:: python

    from pony.orm import Required, db_session, show
    from pony_database_facade import DatabaseFacade


    db = DatabaseFacade()


    class Person(db.Entity):
        username = Required(str, 50)


    db.connect()

    with db_session:
        person_1 = Person(username='Linus')

    show(person_1)


.. |PyPI| image:: https://img.shields.io/pypi/v/pony-database-facade.svg
   :target: https://pypi.python.org/pypi/pony-database-facade/
   :alt: Latest Version

.. |LICENCE| image:: https://img.shields.io/github/license/kyzima-spb/pony-database-facade.svg
   :target: https://github.com/kyzima-spb/pony-database-facade/blob/master/LICENSE
   :alt: Apache 2.0

.. |STARS| image:: https://img.shields.io/github/stars/kyzima-spb/pony-database-facade.svg
   :target: https://github.com/kyzima-spb/pony-database-facade/stargazers

.. _Русская документация: docs/RU.rst
.. _generate_mapping: https://docs.ponyorm.com/api_reference.html#Database.generate_mapping
