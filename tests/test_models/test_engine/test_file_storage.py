#!/usr/bin/python3
"""
Has the TestFileStorageDocumentatins classes an methods
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to see if the documentation and styles of FileStorage class methods"""
    @classmethod
    def setUpClass(cls):
        """setting up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that path to the file_st(models/engine/file_storage.py) aligns with PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test path to test_file_storage.py(tests/test_models/test_file_storage.py) aligns with PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the path to file_storage.py(file_storage.py) module string documentation"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FS class method string documentation"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FS class method needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FS class method needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the existance of the strings documentation
        in FileStorage methods
        """
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t == 'db', "not testing file storage")
class TestFileStorage(unittest.TestCase):
    """Test the FS class instance"""
    def test_all_returns_dict(self):
        """Test that all function brings back the FileStorage.__objects attrib"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    def test_new(self):
        """test that brand new adds a single object to the FileStorage.__objects attrib"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    def test_save(self):
        """Test that it saves properly and saves the objts to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    def test_get(self):
        """test that get brings back an object class by id."""
        storage = models.storage
        obj = State(name='State')
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
        """test that sums up(counts) and returns the no. of objcts of a specific class."""
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
        Amenity(name='Free ammenities').save()
        self.assertGreater(storage.count(), storage.count(State))
        with self.assertRaises(TypeError):
            storage.count(State, 'op')
