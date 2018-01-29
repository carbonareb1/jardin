import unittest
import pandas as pd

from tests import transaction
from models import JardinTestModel


class User(JardinTestModel): pass


class TestModel(unittest.TestCase):

    @transaction(model=User)
    def test_created_at_updated_at(self):
        user = User.insert(values={'name': 'Jardinier'})
        user2 = User.insert(values={'name': 'Jardinier 2'})
        self.assertNotEqual(user.name, user2.name)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        updated_user = User.update(
            values={'name': 'Jardinier 2'},
            where={'id': user.id}
            )
        self.assertTrue(updated_user.updated_at > user.updated_at)
        self.assertEqual(updated_user.created_at, user.created_at)

    @transaction(model=User, create_table=False)
    def test_no_created_at_updated_at(self):
        User.query(
            sql='CREATE TABLE users (id serial PRIMARY KEY, name varchar(256));'
            )
        user = User.insert(values={'name': 'Jardinier'})
        self.assertEqual(User.count(), 1)
        self.assertFalse('updated_at' in user.attributes)
        self.assertFalse('created_at' in user.attributes)

    @transaction(model=User)
    def test_empty_insert(self):
        User.insert(values={})
        self.assertEqual(User.count(), 1)
        User.insert(values=pd.DataFrame())
        self.assertEqual(User.count(), 1)

    @transaction(model=User)
    def test_count(self):
        self.assertEqual(User.count(), 0)
        User.insert(values={'name': 'Holberton'})
        self.assertEqual(User.count(), 1)

    @transaction(model=User)
    def test_custom_count(self):
        User.insert(values={'name': 'Holberton'})
        User.insert(values={'name': 'Holberton'})
        self.assertEqual(User.count(select='DISTINCT(name)'), 1)

    #def test_index_by(self):
    #    users = User({'name': ['John', 'Paul']})
    #    indexed = users.index_by('name')
    #    self.assertEqual(len(indexed), 2)
    #    self.assertIsInstance(indexed['John'], Users.record_class)
    #    self.assertIsInstance(indexed['Paul'], Users.record_class)
    #    self.assertEqual(indexed['Paul'].name, 'Paul')


if __name__ == "__main__":
    unittest.main()
