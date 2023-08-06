🥜 peanutdb
============

A JSON based database for quick prototyping and playing.

.. image:: https://img.shields.io/badge/pypi-v0.2.0-yellow.svg?style=flat-square
        :target: https://pypi.python.org/pypi/peanutdb

Installation
------------

.. code-block:: bash

    $ pip install peanutdb


Or clone the repo:

.. code-block:: bash

    $ git clone https://github.com/ahmednooor/peanutdb.git
    
and copy `peanutdb` directory in you project directory.

Usage
-----

.. code-block:: python

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

    # or you can create a table without any schema like so,
    db.create_table(
        table_name="Table_Name"
    )

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
    # result will always be a list of dicts even if there is only one matched item

    # you can select all items from a table like so,
    result = db.select(
        table_name="Users"
    )

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

    # in case of error or failure, `None` is returned.


Meta
----
Source: https://github.com/ahmednooor/peanutdb

Author: Ahmed Noor

License: MIT
