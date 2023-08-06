"""
PeanutDB
-- A JSON based database for quick prototyping and playing.
- Author: Ahmed Noor
- Source Code: https://github.com/ahmednooor/peanutdb
"""
import os
import uuid
import json


class PeanutDB:
    """PeanutDB Class"""

    def __init__(self, db_path=None):
        """init method"""
        self._db_path = db_path
        self._db = {}
        self._db["__schemas__"] = {}
        # ---
        self._load_db()

    def _load_db(self):
        """load db file"""
        if (self._db_path is not None and
                os.path.isfile(self._db_path) and
                os.path.getsize(self._db_path) > 0):
            with open(self._db_path, "r") as infile:
                self._db = json.load(infile)
            # ---
            if "__schemas__" not in self._db:
                self._db["__schemas__"] = {}

    def _write_db(self):
        """write db file"""
        if self._db_path is not None:
            with open(self._db_path, "w") as outfile:
                json.dump(self._db, outfile, indent=None)

    def _schema_check(self, table_name, field_name, value):
        """check value with schema"""
        type_checked = False
        unique_checked = False
        notnull_checked = False
        try:
            if (
                    self._db["__schemas__"][table_name][field_name]["type"] == "any" or
                    self._db["__schemas__"][table_name] is None):
                type_checked = True
            elif (
                    self._db["__schemas__"][table_name][field_name]["type"] == "number" and
                    isinstance(value, int) or isinstance(value, float)):
                type_checked = True
            elif (
                    self._db["__schemas__"][table_name][field_name]["type"] == "text" and
                    isinstance(value, str)):
                type_checked = True
            elif (
                    self._db["__schemas__"][table_name][field_name]["type"] == "boolean" and
                    isinstance(value, bool)):
                type_checked = True
            elif (
                    self._db["__schemas__"][table_name][field_name]["type"] == "list" and
                    isinstance(value, list)):
                type_checked = True
            elif (
                    self._db["__schemas__"][table_name][field_name]["type"] == "dict" and
                    isinstance(value, dict)):
                type_checked = True
            elif (
                    self._db["__schemas__"][table_name][field_name]["notnull"] is False and
                    value is None):
                type_checked = True
            else:
                return None
            # ---
            if self._db["__schemas__"][table_name][field_name]["unique"] is True:
                for data_item in self._db[table_name]:
                    if field_name in data_item and data_item[field_name] == value:
                        return None
                unique_checked = True
            else:
                unique_checked = True
            # ---
            if (self._db["__schemas__"][table_name][field_name]["notnull"] is True and
                    value is None):
                return None
            else:
                notnull_checked = True
            # ---
            return (
                type_checked is True and
                unique_checked is True and
                notnull_checked is True
            )
        except KeyError:
            return None

    def create_table(self, table_name, schema=None):
        """
        PeanutDB.create_table(
            table_name="Table_Name",
            schema={
                "field_name": {
                    "type": "number"/"text"/"boolean"/"list"/"dict"/"any",
                    "unique": True/False,
                    "notnull": True/False
                },
                ...
            }
        )
        """
        if (table_name in self._db["__schemas__"] or
                table_name in self._db):
            return None
        # ---
        if (table_name == "" or
                not isinstance(table_name, str)):
            return None
        # ---
        if schema is None:
            self._db["__schemas__"][table_name] = None
        else:
            for field_name in schema:
                if (
                        schema[field_name]["type"] not in ["number", "text", "boolean",
                                                           "list", "dict", "any"] or
                        schema[field_name]["unique"] not in [True, False] or
                        schema[field_name]["notnull"] not in [True, False]):
                    return None
            # ---
            schema["__ID"] = {
                "type": "text",
                "unique": True,
                "notnull": True
            }
            self._db["__schemas__"][table_name] = schema
        # ---
        self._db[table_name] = []
        self._write_db()
        return self._db["__schemas__"][table_name]

    def delete_table(self, table_name):
        """
        PeanutDB.delete_table(
            table_name="Table_Name"
        )
        """
        if table_name in self._db["__schemas__"]:
            del self._db["__schemas__"][table_name]
        # ---
        deleted_table = None
        if table_name in self._db:
            deleted_table = self._db[table_name]
            del self._db[table_name]
        # ---
        self._write_db()
        return deleted_table

    def insert(self, table_name, fields):
        """
        PeanutDB.insert(
            table_name="Table_Name",
            fields={
                "field_name": <value>,
                ...
            }
        )
        """
        data = fields
        if table_name not in self._db["__schemas__"] or table_name not in self._db:
            return None
        # ---
        if (
                table_name in self._db["__schemas__"] and
                self._db["__schemas__"][table_name] is not None):
            new_data = {}
            # ---
            for field in self._db["__schemas__"][table_name]:
                if field in data:
                    new_data[field] = data[field]
                else:
                    new_data[field] = None
            # ---
            new_data["__ID"] = str(uuid.uuid4())
            # ---
            for field in new_data:
                if field not in self._db["__schemas__"][table_name]:
                    return None
                schema_checked = self._schema_check(table_name, field, new_data[field])
                if not schema_checked:
                    return None
        else:
            new_data = data
            new_data["__ID"] = str(uuid.uuid4())
        # ---
        self._db[table_name].append(new_data)
        self._write_db()
        # ---
        return self.select(table_name=table_name, where=new_data)

    def select(self, table_name, where=None):
        """
        PeanutDB.select(
            table_name="Table_Name",
            where={
                "field_name": <value>,
                ...
            }
        )
        """
        params = where
        if table_name not in self._db["__schemas__"] or table_name not in self._db:
            return None
        if where is None:
            return self._db[table_name]
        # ---
        searched_items = []
        # ---
        item_matched = False
        for data_item in self._db[table_name]:
            for param in params:
                if param in data_item and params[param] == data_item[param]:
                    item_matched = True
                else:
                    item_matched = False
                    break
            if item_matched is True:
                searched_items.append(data_item)
                item_matched = False
        # ---
        searched_items_length = len(searched_items)
        if searched_items_length > 0:
            return searched_items
        # ---
        return None

    def update(self, table_name, fields, where):
        """
        PeanutDB.update(
            table_name="Table_Name",
            fields={
                "field_name": <value>,
                ...
            },
            where={
                "field_name": <value>,
                ...
            }
        )
        """
        params = where
        data = fields
        if table_name not in self._db["__schemas__"] or table_name not in self._db:
            return None
        # ---
        if (
                table_name in self._db["__schemas__"] and
                self._db["__schemas__"][table_name] is not None):
            new_data = data
            # ---
            for field in new_data:
                if field not in self._db["__schemas__"][table_name]:
                    return None
                schema_checked = self._schema_check(table_name, field, new_data[field])
                if not schema_checked:
                    return None
        else:
            new_data = data
        # ---
        item_matched = False
        for index, data_item in enumerate(self._db[table_name]):
            for param in params:
                if param in data_item and params[param] == data_item[param]:
                    item_matched = True
                else:
                    item_matched = False
                    break
            if item_matched is True:
                for field in new_data:
                    if self._db["__schemas__"][table_name] is None:
                        self._db[table_name][index][field] = new_data[field]
                    elif field in data_item:
                        self._db[table_name][index][field] = new_data[field]
                item_matched = False
        # ---
        self._write_db()
        # ---
        return self.select(table_name=table_name, where=new_data)

    def delete(self, table_name, where):
        """
        PeanutDB.delete(
            table_name="Table_Name",
            where={
                "field_name": <value>,
                ...
            }
        )
        """
        params = where
        if table_name not in self._db["__schemas__"] or table_name not in self._db:
            return None
        # ---
        removed_items = []
        saved_items = []
        # ---
        item_matched = False
        for index, data_item in enumerate(self._db[table_name]):
            for param in params:
                if param in data_item and params[param] == data_item[param]:
                    item_matched = True
                else:
                    item_matched = False
                    break
            if item_matched is True:
                removed_items.append(data_item)
            else:
                saved_items.append(self._db[table_name][index])
        # ---
        self._db[table_name] = saved_items
        # ---
        removed_items_length = len(removed_items)
        if removed_items_length > 0:
            self._write_db()
            return removed_items
        # ---
        return None
