# jardin

Jardin is a `pandas.DataFrame`-based ORM for Python applications.

## Getting started

In your working directory (the root of your app), create a file named `jardin_conf.py`:
```python
# jardin_conf.py

DATABASES = {
  'my_first_database': 'https://username:password@database.url:port',
  'my_second_database': 'https://username:password@database.url:port'
}
```
Then, in your app, say you have a table called `users`:
```python
# app.py
import jardin

class Users(jardin.Model):
  db_names = {'read': 'my_first_database', 'write': 'my_second_database'}
```
In the console:
```python
>>> from app import Users
>>> users = Users.last(4)
# SELECT * FROM users ORDER BY created_at DESC LIMIT 4
>> users
id   name    email              ...
0    John    john@beatl.es      ...
1    Paul    paul@beatl.es      ...
2    George  george@beatl.es    ...
3    Ringo   ringo@beatl.es     ...
```