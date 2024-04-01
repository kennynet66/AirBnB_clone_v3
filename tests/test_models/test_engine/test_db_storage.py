#!/usr/bin/python3
"""
Contains the classes belonging to TestDBStorageDocuments and TestDBStorage 
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to see if the documentation and styles of the DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Setting up for the strorage documents tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that path to storage.py(models/engine/db_storage.py) aligns with PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test path to storage(tests/test_models/test_db_storage.py)
        aligns with PEP8.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py(storage file)
        module string documentation"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage(storage file) class string documentation"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Tests for the availability of string
        documentation in DBStorage class methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the FS class method"""
    def test_all_returns_dict(self):
        """Test that all function returns a tuple"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that it returns all rows when no class-metthod is passed"""

    def test_new(self):
        """test that a brand new and adds a single object to the db"""

    def test_save(self):
        """Test that save properly saves an object to file.json"""

    def test_get(self):
        """Tests that get returns an object class by Id."""
        storage = models.storage
        obj = State(name='Michigan')
        obj.save()
        self.assertEqual(obj.id, storage.get(State, obj.id).id)
        self.assertEqual(obj.name, storage.get(State, obj.id).name)
        self.assertIsNot(obj, storage.get(State, obj.id + 'op'))
        self.assertIsNone(storage.get(State, obj.id + 'op'))
        self.assertIsNone(storage.get(State, 45))
        self.assertIsNone(storage.get(None, obj.id))
        self.assertIsNone(storage.get(int, obj.id))
        with self.assertRaises(TypeError):
            storage.get(State, obj.id, 'op')
        with self.assertRaises(TypeError):
            storage.get(State)
        with self.assertRaises(TypeError):
            storage.get()

    def test_count(self):
        """
        A test that adds up(counts) and returns
        the no. of objects of a certain class instance.
        """
        storage = models.storage
        self.assertIs(type(storage.count()), int)
        self.assertIs(type(storage.count(None)), int)
        self.assertIs(type(storage.count(int)), int)
        self.assertIs(type(storage.count(State)), int)
        self.assertEqual(storage.count(), storage.count(None))
        State(name='State').save()
        self.assertGreater(storage.count(State), 0)
        self.assertEqual(storage.count(), storage.count(None))
        a = storage.count(State)
        State(name='Town').save()
        self.assertGreater(storage.count(State), a)
        Amenity(name='Free Amenities').save()
        self.assertGreater(storage.count(), storage.count(State))
        with self.assertRaises(TypeError):
            storage.count(State, 'op')
