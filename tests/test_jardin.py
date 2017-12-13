import unittest
from models import JardinTestModel


class Users(JardinTestModel): pass


class TestTransaction(object):

    def __init__(self, model):
        self._model = model
        self._connection = self._model.db(role='master')

    def __enter__(self):
        self._model.query(sql='drop table if exists %s cascade;' % self._model.model_metadata()['table_name'])
        self._model._columns = None
        self._connection.autocommit = False
        self._model.query(sql='BEGIN;', role='master')

    def __exit__(self, exc_type, exc_value, traceback):
        self._model.query(sql='ROLLBACK;', role='master')
        self._connection.autocommit = True



class TestModel(unittest.TestCase):
    def test_created_at_updated_at(self):
        with TestTransaction(Users):
            Users.query(
                sql='CREATE TABLE users (id serial PRIMARY KEY, name varchar(256), created_at timestamp, updated_at timestamp);'
                )
            user = Users.insert(values={'name': 'Jardinier'})
            self.assertIsNotNone(user.created_at)
            self.assertIsNotNone(user.updated_at)
            updated_user = Users.update(
                values={'name': 'Jardinier 2'},
                where={'id': user.id}
                )
            self.assertTrue(updated_user.updated_at > user.updated_at)
            self.assertEqual(updated_user.created_at, user.created_at)

    def test_no_created_at_updated_at(self):
        with TestTransaction(Users):
            Users.query(
                sql='CREATE TABLE users (id serial PRIMARY KEY, name varchar(256));'
                )
            user = Users.insert(values={'name': 'Jardinier'})
            self.assertEqual(Users.count(), 1)
            self.assertFalse('updated_at' in user)
            self.assertFalse('created_at' in user)