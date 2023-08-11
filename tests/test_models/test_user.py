#!/usr/bin/python3
"""defines unittests for models/user.py.

Unittest classes:
    TestUser_yinstantiation
    TestUser_ysave
    TestUser_to_ydict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_yinstantiation(unittest.TestCase):
    """Unittests test instantiation of User class."""

    def test_no_args_yinstantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_ystored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_ypublic_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_ypublic_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_ypublic_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_ypublic_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_ypublic_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_ypublic_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_ypublic_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_yunique_ids(self):
        yus1 = User()
        yus2 = User()
        self.assertNotEqual(yus1.id, yus2.id)

    def test_two_users_ydifferent_created_at(self):
        yus1 = User()
        sleep(0.05)
        yus2 = User()
        self.assertLess(yus1.created_at, yus2.created_at)

    def test_two_users_ydifferent_updated_at(self):
        yus1 = User()
        sleep(0.05)
        yus2 = User()
        self.assertLess(yus1.updated_at, yus2.updated_at)

    def test_str_yrepresentation(self):
        ydt = datetime.today()
        ydt_repr = repr(ydt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = ydt
        yusstr = us.__str__()
        self.assertIn("[User] (123456)", yusstr)
        self.assertIn("'id': '123456'", yusstr)
        self.assertIn("'created_at': " + ydt_repr, yusstr)
        self.assertIn("'updated_at': " + ydt_repr, yusstr)

    def test_args_yunused(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def test_instantiation_ywith_kwargs(self):
        ydt = datetime.today()
        ydt_iso = ydt.isoformat()
        us = User(id="345", created_at=ydt_iso, updated_at=ydt_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at, ydt)
        self.assertEqual(us.updated_at, ydt)

    def test_instantiation_ywith_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_ysave(unittest.TestCase):
    """Unittests test save method of class."""

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

    def test_one_ysave(self):
        us = User()
        sleep(0.05)
        yfirst_updated_at = us.updated_at
        us.save()
        self.assertLess(yfirst_updated_at, us.updated_at)

    def test_two_ysaves(self):
        us = User()
        sleep(0.05)
        yfirst_updated_at = us.updated_at
        us.save()
        ysecond_updated_at = us.updated_at
        self.assertLess(yfirst_updated_at, ysecond_updated_at)
        sleep(0.05)
        us.save()
        self.assertLess(ysecond_updated_at, us.updated_at)

    def test_save_with_yarg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def test_save_yupdates_file(self):
        us = User()
        us.save()
        yusid = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(yusid, f.read())


class TestUser_to_ydict(unittest.TestCase):
    """Unittests testing to_dict method User class."""

    def test_to_dict_ytype(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_ycorrect_keys(self):
        us = User()
        self.assertIn("id", us.to_dict())
        self.assertIn("created_at", us.to_dict())
        self.assertIn("updated_at", us.to_dict())
        self.assertIn("__class__", us.to_dict())

    def test_to_dict_contains_yadded_attributes(self):
        us = User()
        us.middle_name = "Holberton"
        us.my_number = 98
        self.assertEqual("Holberton", us.middle_name)
        self.assertIn("my_number", us.to_dict())

    def test_to_dict_datetime_yattributes_are_strs(self):
        us = User()
        us_dict = us.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    def test_to_dict_youtput(self):
        ydt = datetime.today()
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = ydt
        ytdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': ydt.isoformat(),
            'updated_at': ydt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), ytdict)

    def test_contrast_to_ydict_dunder_dict(self):
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def test_to_dict_ywith_arg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
