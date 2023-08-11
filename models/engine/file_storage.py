#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """handles serialization and deserialization of BaseModel instance.


    Attributes:
        __file_path (str): The name of file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set __objects obj with key <obj_class_name>.id"""
        yocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(yocname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        yodict = FileStorage.__objects
        yobjdict = {obj: yodict[obj].to_dict() for obj in yodict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(yobjdict, f)

    def reload(self):
        """deserialize JSON file __file_path to __objects, if exists."""
        try:
            with open(FileStorage.__file_path) as f:
                yobjdict = json.load(f)
                for o in yobjdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
