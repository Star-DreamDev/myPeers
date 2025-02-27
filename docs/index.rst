.. peers documentation master file, created by
   sphinx-quickstart on Thu Nov 25 21:20:29 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

peers
======

.. image:: peers-logo.png

Peers is a simple and small ORM. It has few (but expressive) concepts, making
it easy to learn and intuitive to use.

* a small, expressive ORM
* flexible query-builder that exposes full power of SQL
* supports :ref:`sqlite, mysql, mariadb, postgresql <database>`.
* :ref:`asyncio support <pwasyncio>`
* tons of extensions
* use with :ref:`flask <flask>`, :ref:`fastapi <fastapi>`, :ref:`pydantic <pydantic>`
  and :ref:`more <framework-integration>`

Peers's source code hosted on `GitHub <https://github.com/Star-DreamDev/peers>`_.

New to peers? These may help:

* :ref:`Quickstart <quickstart>`
* :ref:`Example twitter app <example>`
* :ref:`Using peers interactively <interactive>`
* :ref:`Models and fields <models>`
* :ref:`Querying <querying>`
* :ref:`Relationships and joins <relationships>`
* :ref:`Extensive library of SQL / Peers examples <query-library>`
* :ref:`Flask setup <flask>` or :ref:`FastAPI setup <fastapi>`

Contents:
---------

.. toctree::
   :maxdepth: 2

   peers/installation
   peers/quickstart
   peers/example
   peers/database
   peers/models
   peers/relationships
   peers/querying
   peers/writing
   peers/query_operators
   peers/transactions
   peers/schema
   peers/asyncio
   peers/framework_integration
   peers/interactive
   peers/query_builder
   peers/query_library
   peers/api
   peers/sqlite
   peers/postgres
   peers/mysql
   peers/json_field
   peers/db_tools
   peers/orm_utils
   peers/recipes
   peers/contributing

Note
----

If you find any bugs, odd behavior, or have an idea for a new feature please
don't hesitate to `open an issue <https://github.com/Star-DreamDev/peers/issues?state=open>`_
on GitHub.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
