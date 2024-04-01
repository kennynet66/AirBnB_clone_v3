#!/usr/bin/python3
"""
Contains the FS class instance
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """ID's instances to a JSON file & de-id's back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the tuple __objcts"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def get(self, cls, id):
        """fetches an objct of a class instance using the Id"""
        if cls is not None:
            res = list(
                filter(
                    lambda x: type(x) is cls and x.id == id,
                    self.__objects.values()
                )
            )
            if res:
                return res[0]
        return None

    def count(self, cls=None):
        """Fetches the no. of objects of a class instance or all (if cls===None)"""
        return len(self.all(cls))

    def new(self, obj):
        """puts in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """ID's __objcts to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """de-ID's the JSON files to __objcts"""
        try:
            with open(self.__file_path, 'r') as f:
                jon = json.load(f)
            for key in jon:
                self.__objects[key] = classes[jon[key]["__class__"]](**jon[key])
        except Exception:
            pass

    def delete(self, objt=None):
        """deletes|Removes obj from __objct if it’s in"""
        if objt is not None:
            key = objt.__class__.__name__ + '.' + objt.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() | refresh() method | fuction for de-id'ing the JSON file to objct"""
        self.reload()
