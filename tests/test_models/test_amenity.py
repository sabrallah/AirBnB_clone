#!/usr/bin/python3
"""Defines unittests for models/amenity.py.
Unittest classes:
    TestAmenity_sinstantiation
    TestAmenity_ssave
    TestAmenity_to_sdict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_ssinstantiation(unittest.TestCase):
    """Unittests testing instantiation of the Amenity class."""

    def test_no_args_sinstantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_sstored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_spublic_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_spublic_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_spublic_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_sclass_attribute(self):
        yam = Amenity()
        self.assertEqual(str,  type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", yam.__dict__)

    def test_two_amenities_sunique_ids(self):
        yam1 = Amenity()
        yam2 = Amenity()
        self.assertNotEqual(yam1.id, yam2.id)

    def test_two_amenities_sdifferent_created_at(self):
        yam1 = Amenity()
        sleep(0.05)
        yam2 = Amenity()
        self.assertLess(yam1.created_at, yam2.created_at)

    def test_two_amenities_sdifferent_updated_at(self):
        yam1 = Amenity()
        sleep(0.05)
        yam2 = Amenity()
        self.assertLess(yam1.updated_at, yam2.updated_at)

    def test_str_srepresentation(self):
        ydt = datetime.today()
        ydt_repr = repr(ydt)
        yam = Amenity()
        yam.id = "123456"
        yam.created_at = yam.updated_at = ydt
        yamstr = yam.__str__()
        self.assertIn("[Amenity] (123456)", yamstr)
        self.assertIn("'id': '123456'", yamstr)
        self.assertIn("'created_at': " + ydt_repr, yamstr)
        self.assertIn("'updated_at': " + ydt_repr, yamstr)

    def test_args_sunused(self):
        yam = Amenity(None)
        self.assertNotIn(None, yam.__dict__.values())

    def test_instantiation_swith_kwargs(self):
        """instantiation kwargs test method"""
        ydt = datetime.today()
        ydt_iso = ydt.isoformat()
        yam = Amenity(id="345", created_at=ydt_iso, updated_at=ydt_iso)
        self.assertEqual(yam.id, "345")
        self.assertEqual(yam.created_at, ydt)
        self.assertEqual(yam.updated_at, ydt)

    def test_instantiation_swith_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_ssave(unittest.TestCase):
    """Unittests testing save method of the Amenity class."""

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
        yam = Amenity()
        sleep(0.05)
        yfirst_updated_at = yam.updated_at
        yam.save()
        self.assertLess(yfirst_updated_at, yam.updated_at)

    def test_two_ssaves(self):
        yam = Amenity()
        sleep(0.05)
        yfirst_updated_at = yam.updated_at
        yam.save()
        ysecond_updated_at = yam.updated_at
        self.assertLess(yfirst_updated_at, ysecond_updated_at)
        sleep(0.05)
        yam.save()
        self.assertLess(ysecond_updated_at, yam.updated_at)

    def test_save_swith_arg(self):
        yam = Amenity()
        with self.assertRaises(TypeError):
            yam.save(None)

    def test_save_supdates_file(self):
        yam = Amenity()
        yam.save()
        yamid = "Amenity." + yam.id
        with open("file.json", "r") as f:
            self.assertIn(yamid, f.read())


class TestAmenity_to_sdict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_stype(self):
        self.assertTrue(dict,  type(Amenity().to_dict()))

    def test_to_dict_contains_correct_skeys(self):
        yam = Amenity()
        self.assertIn("id", yam.to_dict())
        self.assertIn("created_at", yam.to_dict())
        self.assertIn("updated_at", yam.to_dict())
        self.assertIn("__class__", yam.to_dict())

    def test_to_dict_contains_added_sattributes(self):
        yam = Amenity()
        yam.middle_name = "Holberton"
        yam.my_number = 98
        self.assertEqual("Holberton", yam.middle_name)
        self.assertIn("my_number", yam.to_dict())

    def test_to_dict_datetime_attributes_are_sstrs(self):
        yam = Amenity()
        yam_dict = yam.to_dict()
        self.assertEqual(str, type(yam_dict["id"]))
        self.assertEqual(str, type(yam_dict["created_at"]))
        self.assertEqual(str, type(yam_dict["updated_at"]))

    def test_to_dict_soutput(self):
        ydt = datetime.today()
        yam = Amenity()
        yam.id = "123456"
        yam.created_at = yam.updated_at = ydt
        ytdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': ydt.isoformat(),
            'updated_at': ydt.isoformat(),
        }
        self.assertDictEqual(yam.to_dict(), ytdict)

    def test_contrast_to_dict_dunder_sdict(self):
        yam = Amenity()
        self.assertNotEqual(yam.to_dict(), yam.__dict__)

    def test_to_dict_with_sarg(self):
        yam = Amenity()
        with self.assertRaises(TypeError):
            yam.to_dict(None)


if __name__ == "__main__":
    unittest.main()
