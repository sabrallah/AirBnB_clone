#!/usr/bin/python3
"""defines unittests models/engine/file_storage.py.

unittest classes:
    TestFileStorage_yinstantiation
    TestFileStorage_ymethods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_yinstantiation(unittest.TestCase):
    """unittests for testin instantiation FileStorage class."""

    def test_FileStorage_yinstantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_yinstantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_yfile_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_FileStorage_yobjects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_yinitializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_ymethods(unittest.TestCase):
    """unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_y(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_ywith_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_y(self):
        ybm = BaseModel()
        yus = User()
        yst = State()
        ypl = Place()
        ycy = City()
        yam = Amenity()
        yrv = Review()
        models.storage.new(ybm)
        models.storage.new(yus)
        models.storage.new(yst)
        models.storage.new(ypl)
        models.storage.new(ycy)
        models.storage.new(yam)
        models.storage.new(yrv)
        self.assertIn("BaseModel." + ybm.id, models.storage.all().keys())
        self.assertIn(ybm, models.storage.all().values())
        self.assertIn("User." + yus.id, models.storage.all().keys())
        self.assertIn(yus, models.storage.all().values())
        self.assertIn("State." + yst.id, models.storage.all().keys())
        self.assertIn(yst, models.storage.all().values())
        self.assertIn("Place." + ypl.id, models.storage.all().keys())
        self.assertIn(ypl, models.storage.all().values())
        self.assertIn("City." + ycy.id, models.storage.all().keys())
        self.assertIn(ycy, models.storage.all().values())
        self.assertIn("Amenity." + yam.id, models.storage.all().keys())
        self.assertIn(yam, models.storage.all().values())
        self.assertIn("Review." + yrv.id, models.storage.all().keys())
        self.assertIn(yrv, models.storage.all().values())

    def test_new_ywith_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_ywith_None(self):
        # This test checks if an AttributeError is raised
        # This test checks if an AttributeError raised
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_y(self):
        ybm = BaseModel()
        yus = User()
        yst = State()
        ypl = Place()
        ycy = City()
        yam = Amenity()
        yrv = Review()
        models.storage.new(ybm)
        models.storage.new(yus)
        models.storage.new(yst)
        models.storage.new(ypl)
        models.storage.new(ycy)
        models.storage.new(yam)
        models.storage.new(yrv)
        models.storage.save()
        ysave_text = ""
        with open("file.json", "r") as f:
            ysave_text = f.read()
            self.assertIn("BaseModel." + ybm.id, ysave_text)
            self.assertIn("User." + yus.id, ysave_text)
            self.assertIn("State." + yst.id, ysave_text)
            self.assertIn("Place." + ypl.id, ysave_text)
            self.assertIn("City." + ycy.id, ysave_text)
            self.assertIn("Amenity." + yam.id, ysave_text)
            self.assertIn("Review." + yrv.id, ysave_text)

    def test_save_ywith_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_y(self):
        ybm = BaseModel()
        yus = User()
        yst = State()
        ypl = Place()
        ycy = City()
        yam = Amenity()
        yrv = Review()
        models.storage.new(ybm)
        models.storage.new(yus)
        models.storage.new(yst)
        models.storage.new(ypl)
        models.storage.new(ycy)
        models.storage.new(yam)
        models.storage.new(yrv)
        models.storage.save()
        models.storage.reload()
        yobjs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + ybm.id, yobjs)
        self.assertIn("User." + yus.id, yobjs)
        self.assertIn("State." + yst.id, yobjs)
        self.assertIn("Place." + ypl.id, yobjs)
        self.assertIn("City." + ycy.id, yobjs)
        self.assertIn("Amenity." + yam.id, yobjs)
        self.assertIn("Review." + yrv.id, yobjs)

    def test_reload_ywith_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
