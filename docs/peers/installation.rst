.. _installation:

Installing and Testing
======================

Most users will want to simply install the latest version, hosted on PyPI:

.. code-block:: shell
   :emphasize-lines: 1

   pip install peers

Peers has an optional Sqlite C extension which is not bundled as part of the
wheel. If you wish to use this, you can install Peers via source distribution:

.. code-block:: shell

   pip install peers --no-binary :all:

Installing with git
-------------------

The project is hosted at https://github.com/Star-DreamDev/peers and can be installed
using git:

.. code-block:: shell

   git clone https://github.com/Star-DreamDev/peers.git
   cd peers
   pip install .

Running tests
-------------

You can test your installation by running the test suite.

.. code-block:: shell

   python runtests.py

You can test specific features or specific database drivers using the
``runtests.py`` script. To view the available test runner options, use:

.. code-block:: shell

   python runtests.py --help

.. note::
   To run tests against Postgres or MySQL you need to create a database named
   "peers_test". To test the Postgres extension module, you will also want to
   install the HStore extension in the postgres test database:

   .. code-block:: sql

      -- install the hstore extension on the peers_test postgres db.
      CREATE EXTENSION hstore;

Driver support
--------------

+-----------------------+------------------------+--------------------------------------------+
| Database              | Driver                 | Implementation                             |
+=======================+========================+============================================+
| **Sqlite**            | ``sqlite3``            | :py:class:`SqliteDatabase`                 |
+-----------------------+------------------------+--------------------------------------------+
| **Postgres**          | ``psycopg2``           | :py:class:`PostgresqlDatabase`             |
+-----------------------+------------------------+--------------------------------------------+
| **Postgres**          | ``psycopg3``           | :py:class:`PostgresqlDatabase`             |
+-----------------------+------------------------+--------------------------------------------+
| **MySQL**             | ``pymysql``            | :py:class:`MySQLDatabase`                  |
+-----------------------+------------------------+--------------------------------------------+
| Sqlite (async)        | ``aiosqlite``          | :py:class:`AsyncSqliteDatabase`            |
+-----------------------+------------------------+--------------------------------------------+
| Postgres (async)      | ``asyncpg``            | :py:class:`AsyncPostgresqlDatabase`        |
+-----------------------+------------------------+--------------------------------------------+
| MySQL (async)         | ``aiomysql``           | :py:class:`AsyncMySQLDatabase`             |
+-----------------------+------------------------+--------------------------------------------+
| Sqlite (alternate)    | ``cysqlite``           | :py:class:`CySqliteDatabase`               |
+-----------------------+------------------------+--------------------------------------------+
| Sqlite (alternate)    | ``apsw``               | :py:class:`APSWDatabase`                   |
+-----------------------+------------------------+--------------------------------------------+
| SqlCipher             | ``sqlcipher3``         | :py:class:`SqlCipherDatabase`              |
+-----------------------+------------------------+--------------------------------------------+
| MySQL (alternate)     | ``mysql-connector``    | :py:class:`MySQLConnectorDatabase`         |
+-----------------------+------------------------+--------------------------------------------+
| MariaDB (alternate)   | ``mariadb-connector``  | :py:class:`MariaDBConnectorDatabase`       |
+-----------------------+------------------------+--------------------------------------------+
