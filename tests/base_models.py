from peers import *

from .base import TestModel


# Basic FK pair, Person has a compound unique index on (first, last).

class Person(TestModel):
    first = CharField()
    last = CharField()
    dob = DateField(index=True, null=True)

    class Meta:
        indexes = (
            (('first', 'last'), True),
        )


class Note(TestModel):
    author = ForeignKeyField(Person)
    content = TextField()


# Self-referential FK with a CharField primary key.

class Category(TestModel):
    parent = ForeignKeyField('self', backref='children', null=True)
    name = CharField(max_length=20, primary_key=True)


# Two FKs to the same model.

class Relationship(TestModel):
    from_person = ForeignKeyField(Person, backref='relations')
    to_person = ForeignKeyField(Person, backref='related_to')


# Minimal single-field model for transaction and compound-select tests.

class Register(TestModel):
    value = IntegerField()


# Social graph, the suite's workhorse. SQL assertions rely on table 'users'.

class User(TestModel):
    username = CharField()

    class Meta:
        table_name = 'users'


class Account(TestModel):
    email = CharField()
    user = ForeignKeyField(User, backref='accounts', null=True)


class Tweet(TestModel):
    user = ForeignKeyField(User, backref='tweets')
    content = TextField()
    timestamp = TimestampField()


class Favorite(TestModel):
    user = ForeignKeyField(User, backref='favorites')
    tweet = ForeignKeyField(Tweet, backref='favorites')


# Numeric models for window function and aggregation tests.

class Sample(TestModel):
    counter = IntegerField()
    value = FloatField(default=1.0)


class SampleMeta(TestModel):
    sample = ForeignKeyField(Sample, backref='metadata')
    value = FloatField(default=0.0)


# Three-level FK chain for deep join traversal.

class A(TestModel):
    a = TextField()
class B(TestModel):
    a = ForeignKeyField(A, backref='bs')
    b = TextField()
class C(TestModel):
    b = ForeignKeyField(B, backref='cs')
    c = TextField()


# Single (empno) and compound (first, last) conflict targets for upserts.

class Emp(TestModel):
    first = CharField()
    last = CharField()
    empno = CharField(unique=True)

    class Meta:
        indexes = (
            (('first', 'last'), True),
        )


# Unique key with integer defaults for ON CONFLICT DO UPDATE arithmetic.

class OCTest(TestModel):
    a = CharField(unique=True)
    b = IntegerField(default=0)
    c = IntegerField(default=0)


# ON CONFLICT against a partial unique index.

class UKVP(TestModel):
    key = TextField()
    value = IntegerField()
    extra = IntegerField()

    class Meta:
        # Partial index, the WHERE clause must be reflected in the conflict
        # target.
        indexes = [
            SQL('CREATE UNIQUE INDEX "ukvp_kve" ON "ukvp" ("key", "value") '
                'WHERE "extra" > 1')]


# Named unique constraints for ON CONFLICT ON CONSTRAINT.

class KVCon(TestModel):
    key = TextField()
    value = IntegerField()

    class Meta:
        constraints = [
            SQL('CONSTRAINT kvcon_key_uniq UNIQUE (key)'),
            SQL('CONSTRAINT kvcon_value_uniq UNIQUE (value)')]


# Static, callable, and absent field defaults.

class DfltM(TestModel):
    name = CharField()
    dflt1 = IntegerField(default=1)
    dflt2 = IntegerField(default=lambda: 2)
    dfltn = IntegerField(null=True)


# FK to a non-PK unique column. CharField: MySQL cannot FK a TEXT column.

class Package(TestModel):
    barcode = CharField(unique=True)


class PackageItem(TestModel):
    name = CharField()
    package = ForeignKeyField(Package, backref='items', field=Package.barcode)
