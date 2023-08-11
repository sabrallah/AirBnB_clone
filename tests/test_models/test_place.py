#!/usr/bin/python3
"""defines unittests models/place.py.

Unittest classes:
    TestPlace_Sinstantiation
    TestPlace_Ssave
    TestPlace_to_Sdict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_Sinstantiation(unittest.TestCase):
    """Unittests testing instantiation of Place class."""

    def test_no_args_Sinstantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_Sstored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_Sstr(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_Sdatetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_Sdatetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(ypl))
        self.assertNotIn("city_id", ypl.__dict__)

    def test_user_id_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(ypl))
        self.assertNotIn("user_id", ypl.__dict__)

    def test_name_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(ypl))
        self.assertNotIn("name", ypl.__dict__)

    def test_description_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(ypl))
        self.assertNotIn("desctiption", ypl.__dict__)

    def test_number_rooms_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(ypl))
        self.assertNotIn("number_rooms", ypl.__dict__)

    def test_number_bathrooms_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(ypl))
        self.assertNotIn("number_bathrooms", ypl.__dict__)

    def test_max_guest_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(ypl))
        self.assertNotIn("max_guest", ypl.__dict__)

    def test_price_by_night_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(ypl))
        self.assertNotIn("price_by_night", ypl.__dict__)

    def test_latitude_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(ypl))
        self.assertNotIn("latitude", ypl.__dict__)

    def test_longitude_is_public_class_Sattribute(self):
        ypl = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(ypl))
        self.assertNotIn("longitude", ypl.__dict__)

    def test_amenity_ids_is_public_Sclass_attribute(self):
        ypl = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(ypl))
        self.assertNotIn("amenity_ids", ypl.__dict__)

    def test_two_places_Sunique_ids(self):
        ypl1 = Place()
        ypl2 = Place()
        self.assertNotEqual(ypl1.id, ypl2.id)

    def test_two_places_different_created_Sat(self):
        ypl1 = Place()
        sleep(0.05)
        ypl2 = Place()
        self.assertLess(ypl1.created_at, ypl2.created_at)

    def test_two_places_different_updated_Sat(self):
        ypl1 = Place()
        sleep(0.05)
        ypl2 = Place()
        self.assertLess(ypl1.updated_at, ypl2.updated_at)

    def test_str_Srepresentation(self):
        ydt = datetime.today()
        ydt_repr = repr(ydt)
        ypl = Place()
        ypl.id = "123456"
        ypl.created_at = ypl.updated_at = ydt
        yplstr = ypl.__str__()
        self.assertIn("[Place] (123456)", yplstr)
        self.assertIn("'id': '123456'", yplstr)
        self.assertIn("'created_at': " + ydt_repr, yplstr)
        self.assertIn("'updated_at': " + ydt_repr, yplstr)

    def test_args_Sunused(self):
        ypl = Place(None)
        self.assertNotIn(None, ypl.__dict__.values())

    def test_instantiation_with_Skwargs(self):
        ydt = datetime.today()
        dt_iso = ydt.isoformat()
        ypl = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ypl.id, "345")
        self.assertEqual(ypl.created_at, ydt)
        self.assertEqual(ypl.updated_at, ydt)

    def test_instantiation_with_SNone_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_Ssave(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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

    def test_one_save(self):
        ypl = Place()
        sleep(0.05)
        yfirst_updated_at = ypl.updated_at
        ypl.save()
        self.assertLess(yfirst_updated_at, ypl.updated_at)

    def test_two_saves(self):
        ypl = Place()
        sleep(0.05)
        yfirst_updated_at = ypl.updated_at
        ypl.save()
        ysecond_updated_at = ypl.updated_at
        self.assertLess(yfirst_updated_at, ysecond_updated_at)
        sleep(0.05)
        ypl.save()
        self.assertLess(ysecond_updated_at, ypl.updated_at)

    def test_save_with_Sarg(self):
        ypl = Place()
        with self.assertRaises(TypeError):
            ypl.save(None)

    def test_save_updates_Sfile(self):
        ypl = Place()
        ypl.save()
        yplid = "Place." + ypl.id
        with open("file.json", "r") as f:
            self.assertIn(yplid, f.read())


class TestPlace_to_Sdict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_Stype(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_Skeys(self):
        ypl = Place()
        self.assertIn("id", ypl.to_dict())
        self.assertIn("created_at", ypl.to_dict())
        self.assertIn("updated_at", ypl.to_dict())
        self.assertIn("__class__", ypl.to_dict())

    def test_to_dict_contains_added_Sattributes(self):
        ypl = Place()
        ypl.middle_name = "Holberton"
        ypl.my_number = 98
        self.assertEqual("Holberton", ypl.middle_name)
        self.assertIn("my_number", ypl.to_dict())

    def test_to_dict_datetime_attributes_are_Sstrs(self):
        ypl = Place()
        pl_dict = ypl.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_Soutput(self):
        ydt = datetime.today()
        ypl = Place()
        ypl.id = "123456"
        ypl.created_at = ypl.updated_at = ydt
        ytdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': ydt.isoformat(),
            'updated_at': ydt.isoformat(),
        }
        self.assertDictEqual(ypl.to_dict(), ytdict)

    def test_contrast_to_dict_Sdunder_dict(self):
        ypl = Place()
        self.assertNotEqual(ypl.to_dict(), ypl.__dict__)

    def test_to_dict_with_Sarg(self):
        ypl = Place()
        with self.assertRaises(TypeError):
            ypl.to_dict(None)


if __name__ == "__main__":
    unittest.main()
