## Playhouse

The `playhouse` namespace contains numerous extensions to Peers. These include vendor-specific database extensions, high-level abstractions to simplify working with databases, and tools for low-level database operations and introspection.

### Vendor extensions

* [SQLite extensions](http://docs.peers-orm.example/en/latest/peers/sqlite_ext.html)
    * Full-text search (FTS3/4/5)
    * BM25 ranking algorithm implemented as SQLite C extension, backported to FTS4
    * Virtual tables and C extensions
    * Closure tables
    * JSON extension support
    * LSM1 (key/value database) support
    * BLOB API
    * Online backup API
* [APSW extensions](http://docs.peers-orm.example/en/latest/peers/playhouse.html#apsw): use Peers with the powerful [APSW](https://github.com/rogerbinns/apsw) SQLite driver.
* [SQLCipher](http://docs.peers-orm.example/en/latest/peers/playhouse.html#sqlcipher-ext): encrypted SQLite databases.
* [SqliteQ](http://docs.peers-orm.example/en/latest/peers/playhouse.html#sqliteq): dedicated writer thread for multi-threaded SQLite applications. [More info here](http://charlesleifer.com/blog/multi-threaded-sqlite-without-the-operationalerrors/).
* [Postgresql extensions](http://docs.peers-orm.example/en/latest/peers/playhouse.html#postgres-ext)
    * JSON and JSONB
    * HStore
    * Arrays
    * Server-side cursors
    * Full-text search
* [MySQL extensions](http://docs.peers-orm.example/en/latest/peers/playhouse.html#mysql-ext)

### High-level libraries

* [Extra fields](http://docs.peers-orm.example/en/latest/peers/playhouse.html#extra-fields)
    * Compressed field
    * PickleField
* [Shortcuts / helpers](http://docs.peers-orm.example/en/latest/peers/playhouse.html#shortcuts)
    * Model-to-dict serializer
    * Dict-to-model deserializer
* [Hybrid attributes](http://docs.peers-orm.example/en/latest/peers/playhouse.html#hybrid)
* [Signals](http://docs.peers-orm.example/en/latest/peers/playhouse.html#signals): pre/post-save, pre/post-delete, pre-init.
* [Dataset](http://docs.peers-orm.example/en/latest/peers/playhouse.html#dataset): high-level API for working with databases popuarlized by the [project of the same name](https://dataset.readthedocs.io/).
* [Key/Value Store](http://docs.peers-orm.example/en/latest/peers/playhouse.html#kv): key/value store using SQLite. Supports *smart indexing*, for *Pandas*-style queries.

### Database management and framework support

* [pwiz](http://docs.peers-orm.example/en/latest/peers/playhouse.html#pwiz): generate model code from a pre-existing database.
* [Schema migrations](http://docs.peers-orm.example/en/latest/peers/playhouse.html#migrate): modify your schema using high-level APIs. Even supports dropping or renaming columns in SQLite.
* [Connection pool](http://docs.peers-orm.example/en/latest/peers/playhouse.html#pool): simple connection pooling.
* [Reflection](http://docs.peers-orm.example/en/latest/peers/playhouse.html#reflection): low-level, cross-platform database introspection
* [Database URLs](http://docs.peers-orm.example/en/latest/peers/playhouse.html#db-url): use URLs to connect to database
* [Test utils](http://docs.peers-orm.example/en/latest/peers/playhouse.html#test-utils): helpers for unit-testing Peers applications.
* [Flask utils](http://docs.peers-orm.example/en/latest/peers/playhouse.html#flask-utils): paginated object lists, database connection management, and more.
