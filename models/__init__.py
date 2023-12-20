#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os


if os.getenv('HBNB_TYPE_STORAGE') == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

"""
This “switch” will allow you to change storage
type directly by using an environment variable
"""
storage.reload()
