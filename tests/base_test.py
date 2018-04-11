"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    # runs once for entire testcase
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False  # чтоб не падало из-за ошибки инициализации БД после выполнения запроса
        app.config['PROPAGATE_EXCEPTIONS'] = True # чтоб не было 500 ошибки вместо 401 (@app.errorhandler(JWTError))
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # Make sure database exists

        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client  # create a new test client an reuse the same test client on every test
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
