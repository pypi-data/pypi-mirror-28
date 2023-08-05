peanutdb
===============================

A JSON based database for quick prototyping and playing.

Version: 0.1.1

Installation
------------

To install use pip:

    $ pip install peanutdb


Or clone the repo:

    $ git clone https://github.com/ahmednooor/peanutdb.git
    
    $ python setup.py install

Usage
-----
```python

from peanutdb import PeanutDB

db = PeanutDB("path/to/db.json")
# or db = PeanutDB() for in-memory

db.create_table(
    table_name="Users",
    schema={
        "username": {"type": "text", "unique": True, "notnull": True},
        "name": {"type": "text", "unique": False, "notnull": True}
    }
)
# "__ID" field is automatically added to schema as primary key
# like so, "__ID": {"type": "text", "unique": True, "notnull": True}
# Data Types: "text", "number", "boolean", "list", "dict", "any"

db.insert(
    table_name="Users",
    fields={
        "username": "john",
        "name": "John Doe"
    }
)
# "__ID" field is automatically inserted as primary key using `uuid.uuid4()`

result = db.select(
    table_name="Users",
    where={
        "username": "john"
    }
)
print(result)
# db.select(table_name="Users") to get all items from a table.

db.update(
    table_name="Users",
    fields={
        "name": "Johnathon Doe"
    },
    where={
        "username": "john"
    }
)

db.delete(
    table_name="Users",
    where={
        "username": "john"
    }
)

db.delete_table(
    table_name="Users"
)

```

Meta
----
Source: https://github.com/ahmednooor/peanutdb

Author: Ahmed Noor