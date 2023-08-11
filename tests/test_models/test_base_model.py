#!/usr/bin/python3
"""defines unittests models/base_model.py.

Unittest classes:
    TestBaseModel_sinstantiation
    TestBaseModel_ssave
    TestBaseModel_to_sdict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_sinstantiation(unittest.TestCase):
    """Unittests testing instantiation the BaseModel class."""

    def test_no_args_sinstantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_sobjects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_sstr(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_sdatetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_sdatetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_sids(self):
        ybm1 = BaseModel()
        ybm2 = BaseModel()
        self.assertNotEqual(ybm1.id, ybm2.id)

    def test_two_models_different_created_sat(self):
        ybm1 = BaseModel()
        sleep(0.05)
        ybm2 = BaseModel()
        self.assertLess(ybm1.created_at, ybm2.created_at)

    def test_two_models_different_updated_sat(self):
        ybm1 = BaseModel()
        sleep(0.05)
        ybm2 = BaseModel()
        self.assertLess(ybm1.updated_at, ybm2.updated_at)

    def test_str_srepresentation(self):
        ydt = datetime.today()
        ydt_repr = repr(ydt)
        ybm = BaseModel()
        ybm.id = "123456"
        ybm.created_at = ybm.updated_at = ydt
        ybmstr = ybm.__str__()
        self.assertIn("[BaseModel] (123456)", ybmstr)
        self.assertIn("'id': '123456'", ybmstr)
        self.assertIn("'created_at': " + ydt_repr, ybmstr)
        self.assertIn("'updated_at': " + ydt_repr, ybmstr)

    def test_args_sunused(self):
        ybm = BaseModel(None)
        self.assertNotIn(None, ybm.__dict__.values())

    def test_instantiation_with_skwargs(self):
        ydt = datetime.today()
        dt_iso = ydt.isoformat()
        ybm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ybm.id, "345")
        self.assertEqual(ybm.created_at, ydt)
        self.assertEqual(ybm.updated_at, ydt)

    def test_instantiation_with_None_skwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_skwargs(self):
        ydt = datetime.today()
        dt_iso = ydt.isoformat()
        ybm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ybm.id, "345")
        self.assertEqual(ybm.created_at, ydt)
        self.assertEqual(ybm.updated_at, ydt)


class TestBaseModel_ssave(unittest.TestCase):
    """Unittests testing BaseModel class."""

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

    def test_one_ssave(self):
        ybm = BaseModel()
        sleep(0.05)
        yfirst_updated_at = ybm.updated_at
        ybm.save()
        self.assertLess(yfirst_updated_at, ybm.updated_at)

    def test_two_ssaves(self):
        ybm = BaseModel()
        sleep(0.05)
        yfirst_updated_at = ybm.updated_at
        ybm.save()
        ysecond_updated_at = ybm.updated_at
        self.assertLess(yfirst_updated_at, ysecond_updated_at)
        sleep(0.05)
        ybm.save()
        self.assertLess(ysecond_updated_at, ybm.updated_at)

    def test_save_swith_arg(self):
        ybm = BaseModel()
        with self.assertRaises(TypeError):
            ybm.save(None)

    def test_save_supdates_file(self):
        ybm = BaseModel()
        ybm.save()
        ybmid = "BaseModel." + ybm.id
        with open("file.json", "r") as f:
            self.assertIn(ybmid, f.read())


class TestBaseModel_to_sdict(unittest.TestCase):
    """Unittests testing to_dict method of the BaseModel class."""

    def test_to_sdict_type(self):
        ybm = BaseModel()
        self.assertTrue(dict, type(ybm.to_dict()))

    def test_to_dict_scontains_correct_keys(self):
        ybm = BaseModel()
        self.assertIn("id", ybm.to_dict())
        self.assertIn("created_at", ybm.to_dict())
        self.assertIn("updated_at", ybm.to_dict())
        self.assertIn("__class__", ybm.to_dict())

    def test_to_dict_scontains_added_attributes(self):
        ybm = BaseModel()
        ybm.name = "Holberton"
        ybm.my_number = 98
        self.assertIn("name", ybm.to_dict())
        self.assertIn("my_number", ybm.to_dict())

    def test_to_dict_datetime_sattributes_are_strs(self):
        ybm = BaseModel()
        bm_dict = ybm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_soutput(self):
        ydt = datetime.today()
        ybm = BaseModel()
        ybm.id = "123456"
        ybm.created_at = ybm.updated_at = ydt
        ytdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': ydt.isoformat(),
            'updated_at': ydt.isoformat()
        }
        self.assertDictEqual(ybm.to_dict(), ytdict)

    def test_contrast_to_dict_sdunder_dict(self):
        ybm = BaseModel()
        self.assertNotEqual(ybm.to_dict(), ybm.__dict__)

    def test_to_dict_swith_arg(self):
        ybm = BaseModel()
        with self.assertRaises(TypeError):
            ybm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
