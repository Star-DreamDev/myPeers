from flask import Flask
from jinja2 import DictLoader
from werkzeug.exceptions import NotFound

from peers import *
from playhouse.flask_utils import FlaskDB
from playhouse.flask_utils import PaginatedQuery
from playhouse.flask_utils import get_object_or_404
from playhouse.flask_utils import object_list

from .base import BaseTestCase
from .base import ModelTestCase
from .base import TestModel
from .base import get_in_memory_db


class User(TestModel):
    username = CharField()


TEMPLATES = {
    'users.html': ('{% for user in object_list %}{{ user.username }},'
                   '{% endfor %}'
                   '|{{ page }}|{{ pagination.get_page_count() }}'),
    'custom.html': '{% for u in users %}{{ u.username }};{% endfor %}',
}


class BaseFlaskTestCase(ModelTestCase):
    database = get_in_memory_db()
    requires = [User]

    def setUp(self):
        super(BaseFlaskTestCase, self).setUp()
        for i in range(10):
            User.create(username='u%02d' % i)
        self.app = Flask(__name__)
        self.app.jinja_loader = DictLoader(TEMPLATES)


class TestPaginatedQuery(BaseFlaskTestCase):
    def test_query_or_model(self):
        pq = PaginatedQuery(User, 4)
        self.assertTrue(pq.model is User)
        self.assertEqual(pq.get_page_count(), 3)

        query = User.select().where(User.username < 'u03')
        pq = PaginatedQuery(query, 2)
        self.assertTrue(pq.model is User)
        self.assertTrue(pq.query is query)
        self.assertEqual(pq.get_page_count(), 2)

    def test_get_page(self):
        query = User.select().order_by(User.username)
        pq = PaginatedQuery(query, 4)

        with self.app.test_request_context('/?page=2'):
            self.assertEqual(pq.get_page(), 2)
            self.assertEqual([u.username for u in pq.get_object_list()],
                             ['u04', 'u05', 'u06', 'u07'])

        # Missing, out-of-range and non-numeric values all give page 1.
        for value in ('', '0', '-1', 'xxx'):
            with self.app.test_request_context('/?page=%s' % value):
                self.assertEqual(pq.get_page(), 1)

    def test_page_var(self):
        pq = PaginatedQuery(User, 4, page_var='p')
        with self.app.test_request_context('/?p=3&page=2'):
            self.assertEqual(pq.get_page(), 3)

    def test_explicit_page(self):
        # An explicit page is used instead of reading the request.
        query = User.select().order_by(User.username)
        pq = PaginatedQuery(query, 4, page=3)
        with self.app.test_request_context('/?page=1'):
            self.assertEqual(pq.get_page(), 3)
            self.assertEqual([u.username for u in pq.get_object_list()],
                             ['u08', 'u09'])

    def test_check_bounds(self):
        query = User.select().order_by(User.username)

        pq = PaginatedQuery(query, 3)
        with self.app.test_request_context('/?page=5'):
            self.assertEqual(list(pq.get_object_list()), [])

        pq = PaginatedQuery(query, 3, check_bounds=True)
        with self.app.test_request_context('/?page=4'):
            self.assertEqual([u.username for u in pq.get_object_list()],
                             ['u09'])
        with self.app.test_request_context('/?page=5'):
            self.assertRaises(NotFound, pq.get_object_list)

    def test_get_page_range(self):
        pq = PaginatedQuery(User, 3)
        self.assertEqual(pq.get_page_range(4, 10), [2, 3, 4, 5, 6])
        self.assertEqual(pq.get_page_range(1, 10), [1, 2, 3, 4, 5])
        self.assertEqual(pq.get_page_range(10, 10), [6, 7, 8, 9, 10])
        self.assertEqual(pq.get_page_range(2, 3), [1, 2, 3])
        self.assertEqual(pq.get_page_range(4, 10, show=3), [3, 4, 5])


class TestViewHelpers(BaseFlaskTestCase):
    def test_object_list(self):
        query = User.select().order_by(User.username)
        with self.app.test_request_context('/?page=2'):
            html = object_list('users.html', query, paginate_by=4)
        self.assertEqual(html, 'u04,u05,u06,u07,|2|3')

    def test_object_list_context_variable(self):
        query = User.select().order_by(User.username)
        with self.app.test_request_context('/'):
            html = object_list('custom.html', query, context_variable='users',
                               paginate_by=2)
        self.assertEqual(html, 'u00;u01;')

    def test_object_list_check_bounds(self):
        query = User.select().order_by(User.username)
        with self.app.test_request_context('/?page=4'):
            self.assertRaises(NotFound, object_list, 'users.html', query,
                              paginate_by=4)

    def test_get_object_or_404(self):
        user = get_object_or_404(User, User.username == 'u03')
        self.assertEqual(user.username, 'u03')

        query = User.select().where(User.username < 'u05')
        user = get_object_or_404(query, User.username == 'u04')
        self.assertEqual(user.username, 'u04')

        self.assertRaises(NotFound, get_object_or_404, query,
                          User.username == 'u06')


class TestFlaskDB(BaseTestCase):
    def test_config_dict(self):
        app = Flask(__name__)
        app.config['DATABASE'] = {'name': ':memory:',
                                  'engine': 'peers.SqliteDatabase'}
        flask_db = FlaskDB(app)
        Base = flask_db.Model
        self.assertTrue(isinstance(Base._meta.database, SqliteDatabase))
        self.assertEqual(Base._meta.database.database, ':memory:')

        # Repeated access returns the same base class.
        self.assertTrue(flask_db.Model is Base)

    def test_config_dict_unqualified_engine(self):
        app = Flask(__name__)
        app.config['DATABASE'] = {'name': ':memory:',
                                  'engine': 'SqliteDatabase'}
        db = FlaskDB(app).Model._meta.database
        self.assertTrue(isinstance(db, SqliteDatabase))

    def test_config_dict_extra_params(self):
        app = Flask(__name__)
        app.config['DATABASE'] = {'name': ':memory:',
                                  'engine': 'peers.SqliteDatabase',
                                  'pragmas': {'cache_size': -8000}}
        db = FlaskDB(app).Model._meta.database
        self.assertEqual(db._pragmas, [('cache_size', -8000)])

    def test_database_url(self):
        app = Flask(__name__)
        app.config['DATABASE'] = 'sqlite:///nugget.db'
        db = FlaskDB(app).Model._meta.database
        self.assertTrue(isinstance(db, SqliteDatabase))
        self.assertEqual(db.database, 'nugget.db')

        # An explicit database is used instead of the config value.
        flask_db = FlaskDB(app, 'sqlite:///nuglets.db')
        self.assertEqual(flask_db.Model._meta.database.database, 'nuglets.db')

    def test_database_url_config_key(self):
        app = Flask(__name__)
        app.config['DATABASE_URL'] = 'sqlite:///nugget.db'
        self.assertEqual(FlaskDB(app).Model._meta.database.database,
                         'nugget.db')

    def test_database_instance(self):
        app = Flask(__name__)
        db = SqliteDatabase(':memory:')
        self.assertTrue(FlaskDB(app, db).Model._meta.database is db)

        app.config['DATABASE'] = db
        self.assertTrue(FlaskDB(app).Model._meta.database is db)

    def test_model_class(self):
        class Custom(Model):
            @classmethod
            def hello(cls):
                return 'hello'

        app = Flask(__name__)
        flask_db = FlaskDB(app, SqliteDatabase(':memory:'), model_class=Custom)
        self.assertTrue(issubclass(flask_db.Model, Custom))
        self.assertEqual(flask_db.Model.hello(), 'hello')

    def test_deferred_init(self):
        app = Flask(__name__)
        app.config['DATABASE'] = {'name': ':memory:',
                                  'engine': 'peers.SqliteDatabase'}
        flask_db = FlaskDB()

        Base = flask_db.Model
        model_db = Base._meta.database
        self.assertTrue(isinstance(model_db, Proxy))
        self.assertRaises(AttributeError, lambda: model_db.database)

        class Person(Base):
            name = CharField()

        flask_db.init_app(app)

        # The base class is unchanged and its proxy is now initialized.
        self.assertTrue(flask_db.Model is Base)
        self.assertEqual(model_db.database, ':memory:')
        self.assertTrue(Person._meta.database is model_db)

        Person.create_table()
        for name in ('charlie', 'huey', 'zaizee'):
            Person.create(name=name)
        query = Person.select().order_by(Person.name)
        self.assertEqual([p.name for p in query],
                         ['charlie', 'huey', 'zaizee'])
        model_db.close()

    def test_missing_config(self):
        self.assertRaises(ValueError, FlaskDB, Flask(__name__))

    def test_uninitialized_model_class(self):
        self.assertRaises(RuntimeError, FlaskDB().get_model_class)

    def test_invalid_config_dict(self):
        invalid = (
            {'name': 'x'},                              # No engine.
            {'engine': 'peers.SqliteDatabase'},        # No name.
            {'name': 'x', 'engine': 'nope.NopeDB'},     # Not importable.
            {'name': 'x', 'engine': 'peers.NopeDB'},   # Not an attribute.
            {'name': 'x', 'engine': 'peers.Model'},    # Not a Database.
        )
        for config in invalid:
            app = Flask(__name__)
            app.config['DATABASE'] = config
            self.assertRaises(RuntimeError, FlaskDB, app)


class TestFlaskDBRequestHandlers(BaseTestCase):
    def get_app(self):
        app = Flask(__name__)
        self.db = SqliteDatabase(':memory:')
        self.states = []

        @app.route('/')
        def index():
            self.states.append(self.db.is_closed())
            return 'index'

        @app.route('/logout/')
        def logout():
            self.states.append(self.db.is_closed())
            return 'logout'

        return app

    def test_connect_and_close(self):
        app = self.get_app()
        FlaskDB(app, self.db)

        self.assertTrue(self.db.is_closed())
        self.assertEqual(app.test_client().get('/').data, b'index')

        # The connection was open for the duration of the request only.
        self.assertEqual(self.states, [False])
        self.assertTrue(self.db.is_closed())

    def test_excluded_routes_config(self):
        app = self.get_app()
        app.config['FLASKDB_EXCLUDED_ROUTES'] = ('logout',)
        FlaskDB(app, self.db)

        client = app.test_client()
        client.get('/')
        client.get('/logout/')
        self.assertEqual(self.states, [False, True])
        self.assertTrue(self.db.is_closed())

    def test_excluded_routes_argument(self):
        app = self.get_app()
        FlaskDB(app, self.db, excluded_routes=('logout',))

        client = app.test_client()
        client.get('/logout/')
        client.get('/')
        self.assertEqual(self.states, [True, False])
        self.assertTrue(self.db.is_closed())
