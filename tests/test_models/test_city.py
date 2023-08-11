#!/usr/bin/python3
"""defines unittests models/city.py.

Unittest classes:
    TestCity_sinstantiation
    TestCity_ssave
    TestCity_to_sdict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_sinstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_sinstantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_sobjects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_sstr(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_sdatetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_sdatetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_sattribute(self):
        ycy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(ycy))
        self.assertNotIn("state_id", ycy.__dict__)

    def test_name_is_public_class_sattribute(self):
        ycy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(ycy))
        self.assertNotIn("name", ycy.__dict__)

    def test_two_cities_unique_sids(self):
        ycy1 = City()
        ycy2 = City()
        self.assertNotEqual(ycy1.id, ycy2.id)

    def test_two_cities_different_created_sat(self):
        ycy1 = City()
        sleep(0.05)
        ycy2 = City()
        self.assertLess(ycy1.created_at, ycy2.created_at)

    def test_two_cities_different_updated_sat(self):
        ycy1 = City()
        sleep(0.05)
        ycy2 = City()
        self.assertLess(ycy1.updated_at, ycy2.updated_at)

    def test_str_srepresentation(self):
        ydt = datetime.today()
        ydt_repr = repr(ydt)
        ycy = City()
        ycy.id = "123456"
        ycy.created_at = ycy.updated_at = ydt
        ycystr = ycy.__str__()
        self.assertIn("[City] (123456)", ycystr)
        self.assertIn("'id': '123456'", ycystr)
        self.assertIn("'created_at': " + ydt_repr, ycystr)
        self.assertIn("'updated_at': " + ydt_repr, ycystr)

    def test_args_sunused(self):
        ycy = City(None)
        self.assertNotIn(None, ycy.__dict__.values())

    def test_instantiation_with_skwargs(self):
        ydt = datetime.today()
        ydt_iso = ydt.isoformat()
        ycy = City(id="345", created_at=ydt_iso, updated_at=ydt_iso)
        self.assertEqual(ycy.id, "345")
        self.assertEqual(ycy.created_at, ydt)
        self.assertEqual(ycy.updated_at, ydt)

    def test_instantiation_with_None_skwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_ssave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_ssave(self):
        ycy = City()
        sleep(0.05)
        yfirst_updated_at = ycy.updated_at
        ycy.save()
        self.assertLess(yfirst_updated_at, ycy.updated_at)

    def test_two_ssaves(self):
        ycy = City()
        sleep(0.05)
        yfirst_updated_at = ycy.updated_at
        ycy.save()
        ysecond_updated_at = ycy.updated_at
        self.assertLess(yfirst_updated_at, ysecond_updated_at)
        sleep(0.05)
        ycy.save()
        self.assertLess(ysecond_updated_at, ycy.updated_at)

    def test_save_with_sarg(self):
        ycy = City()
        with self.assertRaises(TypeError):
            ycy.save(None)

    def test_save_updates_sfile(self):
        ycy = City()
        ycy.save()
        ycyid = "City." + ycy.id
        with open("file.json", "r") as f:
            self.assertIn(ycyid, f.read())


class TestCity_to_sdict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_stype(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_skeys(self):
        ycy = City()
        self.assertIn("id", ycy.to_dict())
        self.assertIn("created_at", ycy.to_dict())
        self.assertIn("updated_at", ycy.to_dict())
        self.assertIn("__class__", ycy.to_dict())

    def test_to_dict_contains_added_sattributes(self):
        ycy = City()
        ycy.middle_name = "Holberton"
        ycy.my_number = 98
        self.assertEqual("Holberton", ycy.middle_name)
        self.assertIn("my_number", ycy.to_dict())

    def test_to_dict_datetime_attributes_are_sstrs(self):
        ycy = City()
        ycy_dict = ycy.to_dict()
        self.assertEqual(str, type(ycy_dict["id"]))
        self.assertEqual(str, type(ycy_dict["created_at"]))
        self.assertEqual(str, type(ycy_dict["updated_at"]))

    def test_to_dict_soutput(self):
        ydt = datetime.today()
        ycy = City()
        ycy.id = "123456"
        ycy.created_at = ycy.updated_at = ydt
        ytdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': ydt.isoformat(),
            'updated_at': ydt.isoformat(),
        }
        self.assertDictEqual(ycy.to_dict(), ytdict)

    def test_contrast_to_dict_dunder_sdict(self):
        ycy = City()
        self.assertNotEqual(ycy.to_dict(), ycy.__dict__)

    def test_to_dict_with_sarg(self):
        ycy = City()
        with self.assertRaises(TypeError):
            ycy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
