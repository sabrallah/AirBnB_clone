#!/usr/bin/python3
"""defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_yprompting
    TestHBNBCommand_yhelp
    TestHBNBCommand_yexit
    TestHBNBCommand_ycreate
    TestHBNBCommand_yshow
    TestHBNBCommand_yall
    TestHBNBCommand_ydestroy
    TestHBNBCommand_yupdate
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_yprompting(unittest.TestCase):
    """Unittests testprompting of HBNB ycommand interpreter."""

    def test_prompt_ystring(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_yline(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", youtput.getvalue().strip())


class TestHBNBCommand_yhelp(unittest.TestCase):
    """Unittests test help messages of HBNB ycommand interpreter."""

    def test_help_yquit(self):
        b = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_help_ycreate(self):
        b = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_help_yEOF(self):
        b = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_help_yshow(self):
        b = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_help_ydestroy(self):
        b = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_help_yall(self):
        b = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objects.")
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_help_ycount(self):
        b = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_help_yupdate(self):
        b = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(b, youtput.getvalue().strip())

    def test_yhelp(self):
        b = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(b, youtput.getvalue().strip())


class TestHBNBCommand_yexit(unittest.TestCase):
    """Unittests test exit from HBNB ycommand interpreter."""

    def test_quit_yexits(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_yexits(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_ycreate(unittest.TestCase):
    """Unittests test create from HBNB ycommand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_create_missing_yclass(self):
        ycorrect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_create_yinvalid_class(self):
        ycorrect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_create_yinvalid_syntax(self):
        ycorrect = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        ycorrect = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_create_yobject(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(youtput.getvalue().strip()))
            testKey = "BaseModel.{}".format(youtput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(youtput.getvalue().strip()))
            testKey = "User.{}".format(youtput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(youtput.getvalue().strip()))
            testKey = "State.{}".format(youtput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(youtput.getvalue().strip()))
            testKey = "City.{}".format(youtput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(youtput.getvalue().strip()))
            testKey = "Amenity.{}".format(youtput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(youtput.getvalue().strip()))
            testKey = "Place.{}".format(youtput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(youtput.getvalue().strip()))
            testKey = "Review.{}".format(youtput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


class TestHBNBCommand_yshow(unittest.TestCase):
    """Unittests test show from HBNB ycommand interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_show_ymissing_class(self):
        ycorrect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_show_yinvalid_class(self):
        ycorrect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_show_ymissing_id_space_notation(self):
        ycorrect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_show_ymissing_id_dot_notation(self):
        ycorrect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_show_no_yinstance_found_space_notation(self):
        ycorrect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_show_no_yinstance_found_dot_notation(self):
        ycorrect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_show_objects_yspace_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["BaseModel.{}".format(ytestID)]
            ycommand = "show BaseModel {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["User.{}".format(ytestID)]
            ycommand = "show User {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["State.{}".format(ytestID)]
            ycommand = "show State {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Place.{}".format(ytestID)]
            ycommand = "show Place {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["City.{}".format(ytestID)]
            ycommand = "show City {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Amenity.{}".format(ytestID)]
            ycommand = "show Amenity {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Review.{}".format(ytestID)]
            ycommand = "show Review {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())

    def test_show_objects_yspace_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["BaseModel.{}".format(ytestID)]
            ycommand = "BaseModel.show({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["User.{}".format(ytestID)]
            ycommand = "User.show({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["State.{}".format(ytestID)]
            ycommand = "State.show({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Place.{}".format(ytestID)]
            ycommand = "Place.show({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["City.{}".format(ytestID)]
            ycommand = "City.show({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Amenity.{}".format(ytestID)]
            ycommand = "Amenity.show({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Review.{}".format(ytestID)]
            ycommand = "Review.show({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertEqual(yobj.__str__(), youtput.getvalue().strip())


class TestHBNBCommand_ydestroy(unittest.TestCase):
    """Unittests test destroy from HBNB ycommand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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
        storage.reload()

    def test_destroy_ymissing_class(self):
        ycorrect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_destroy_yinvalid_class(self):
        ycorrect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_destroy_id_ymissing_space_notation(self):
        ycorrect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_destroy_id_ymissing_dot_notation(self):
        ycorrect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_destroy_invalid_id_yspace_notation(self):
        ycorrect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_destroy_invalid_id_ydot_notation(self):
        ycorrect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_destroy_objects_space_ynotation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["BaseModel.{}".format(ytestID)]
            ycommand = "destroy BaseModel {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["User.{}".format(ytestID)]
            ycommand = "show User {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["State.{}".format(ytestID)]
            ycommand = "show State {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Place.{}".format(ytestID)]
            ycommand = "show Place {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["City.{}".format(ytestID)]
            ycommand = "show City {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Amenity.{}".format(ytestID)]
            ycommand = "show Amenity {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Review.{}".format(ytestID)]
            ycommand = "show Review {}".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())

    def test_destroy_objects_dot_ynotation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["BaseModel.{}".format(ytestID)]
            ycommand = "BaseModel.destroy({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["User.{}".format(ytestID)]
            ycommand = "User.destroy({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["State.{}".format(ytestID)]
            ycommand = "State.destroy({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Place.{}".format(ytestID)]
            ycommand = "Place.destroy({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["City.{}".format(ytestID)]
            ycommand = "City.destroy({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Amenity.{}".format(ytestID)]
            ycommand = "Amenity.destroy({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            ytestID = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            yobj = storage.all()["Review.{}".format(ytestID)]
            ycommand = "Review.destory({})".format(ytestID)
            self.assertFalse(HBNBCommand().onecmd(ycommand))
            self.assertNotIn(yobj, storage.all())


class TestHBNBCommand_yall(unittest.TestCase):
    """Unittests test all HBNB ycommand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_all_invalid_yclass(self):
        ycorrect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_all_objects_space_ynotation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", youtput.getvalue().strip())
            self.assertIn("User", youtput.getvalue().strip())
            self.assertIn("State", youtput.getvalue().strip())
            self.assertIn("Place", youtput.getvalue().strip())
            self.assertIn("City", youtput.getvalue().strip())
            self.assertIn("Amenity", youtput.getvalue().strip())
            self.assertIn("Review", youtput.getvalue().strip())

    def test_all_objects_ydot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", youtput.getvalue().strip())
            self.assertIn("User", youtput.getvalue().strip())
            self.assertIn("State", youtput.getvalue().strip())
            self.assertIn("Place", youtput.getvalue().strip())
            self.assertIn("City", youtput.getvalue().strip())
            self.assertIn("Amenity", youtput.getvalue().strip())
            self.assertIn("Review", youtput.getvalue().strip())

    def test_all_single_yobject_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", youtput.getvalue().strip())
            self.assertNotIn("User", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())

    def test_all_single_yobject_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", youtput.getvalue().strip())
            self.assertNotIn("User", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", youtput.getvalue().strip())
            self.assertNotIn("BaseModel", youtput.getvalue().strip())


class TestHBNBCommand_yupdate(unittest.TestCase):
    """Unittests test update from HBNB ycommand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_update_missing_yclass(self):
        ycorrect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_yinvalid_class(self):
        ycorrect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_ymissing_id_space_notation(self):
        ycorrect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_ymissing_id_dot_notation(self):
        ycorrect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_yinvalid_id_space_notation(self):
        ycorrect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_yinvalid_id_dot_notation(self):
        ycorrect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_ymissing_attr_name_space_notation(self):
        ycorrect = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "update BaseModel {}".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "update User {}".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "update State {}".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "update City {}".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "update Amenity {}".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "update Place {}".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_ymissing_attr_name_dot_notation(self):
        ycorrect = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "BaseModel.update({})".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "User.update({})".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "State.update({})".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "City.update({})".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "Amenity.update({})".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            ytestId = youtput.getvalue().strip()
            ytestCmd = "Place.update({})".format(ytestId)
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_ymissing_attr_value_space_notation(self):
        ycorrect = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create BaseModel")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "update BaseModel {} attr_name".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create User")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "update User {} attr_name".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create State")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "update State {} attr_name".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create City")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "update City {} attr_name".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Amenity")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "update Amenity {} attr_name".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "update Place {} attr_name".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Review")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "update Review {} attr_name".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_ymissing_attr_value_dot_notation(self):
        ycorrect = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create BaseModel")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "BaseModel.update({}, attr_name)".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create User")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "User.update({}, attr_name)".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create State")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "State.update({}, attr_name)".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create City")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "City.update({}, attr_name)".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Amenity")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "Amenity.update({}, attr_name)".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "Place.update({}, attr_name)".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Review")
            ytestId = youtput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as youtput:
            ytestCmd = "Review.update({}, attr_name)".format(ytestId)
            self.assertFalse(HBNBCommand().onecmd(ytestCmd))
            self.assertEqual(ycorrect, youtput.getvalue().strip())

    def test_update_valid_ystring_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create BaseModel")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update BaseModel {} attr_name 'attr_value'".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["BaseModel.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create User")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update User {} attr_name 'attr_value'".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["User.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create State")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update State {} attr_name 'attr_value'".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["State.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create City")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update City {} attr_name 'attr_value'".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["City.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Place {} attr_name 'attr_value'".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Amenity")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Amenity {} attr_name 'attr_value'".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Amenity.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Review")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Review {} attr_name 'attr_value'".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Review.{}".format(ytestId)].__dict__
        self.assertTrue("attr_value", ytes_dict["attr_name"])

    def test_update_valid_ystring_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create BaseModel")
            ytId = youtput.getvalue().strip()
        ytestCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["BaseModel.{}".format(ytId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create User")
            ytId = youtput.getvalue().strip()
        ytestCmd = "User.update({}, attr_name, 'attr_value')".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["User.{}".format(ytId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create State")
            ytId = youtput.getvalue().strip()
        ytestCmd = "State.update({}, attr_name, 'attr_value')".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["State.{}".format(ytId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create City")
            ytId = youtput.getvalue().strip()
        ytestCmd = "City.update({}, attr_name, 'attr_value')".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["City.{}".format(ytId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytId = youtput.getvalue().strip()
        ytestCmd = "Place.update({}, attr_name, 'attr_value')".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Place.{}".format(ytId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Amenity")
            ytId = youtput.getvalue().strip()
        ytestCmd = "Amenity.update({}, attr_name, 'attr_value')".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Amenity.{}".format(ytId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Review")
            ytId = youtput.getvalue().strip()
        ytestCmd = "Review.update({}, attr_name, 'attr_value')".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Review.{}".format(ytId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

    def test_update_valid_int_yattr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Place {} max_guest 98".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual(98, ytes_dict["max_guest"])

    def test_update_valid_int_yattr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytId = youtput.getvalue().strip()
        ytestCmd = "Place.update({}, max_guest, 98)".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Place.{}".format(ytId)].__dict__
        self.assertEqual(98, ytes_dict["max_guest"])

    def test_update_valid_float_yattr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Place {} latitude 7.2".format(ytestId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual(7.2, ytes_dict["latitude"])

    def test_update_valid_float_yattr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytId = youtput.getvalue().strip()
        ytestCmd = "Place.update({}, latitude, 7.2)".format(ytId)
        self.assertFalse(HBNBCommand().onecmd(ytestCmd))
        ytes_dict = storage.all()["Place.{}".format(ytId)].__dict__
        self.assertEqual(7.2, ytes_dict["latitude"])

    def test_update_valid_dictionary_yspace_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create BaseModel")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update BaseModel {} ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["BaseModel.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create User")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update User {} ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["User.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create State")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update State {} ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["State.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create City")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update City {} ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["City.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Place {} ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Amenity")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Amenity {} ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Amenity.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Review")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Review {} ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Review.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

    def test_update_valid_ydictionary_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create BaseModel")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "BaseModel.update({}".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["BaseModel.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create User")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "User.update({}, ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["User.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create State")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "State.update({}, ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["State.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create City")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "City.update({}, ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["City.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "Place.update({}, ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Amenity")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "Amenity.update({}, ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Amenity.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Review")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "Review.update({}, ".format(ytestId)
        ytestCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Review.{}".format(ytestId)].__dict__
        self.assertEqual("attr_value", ytes_dict["attr_name"])

    def test_update_valid_dictionary_ywith_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Place {} ".format(ytestId)
        ytestCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual(98, ytes_dict["max_guest"])

    def test_update_valid_ydictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "Place.update({}, ".format(ytestId)
        ytestCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual(98, ytes_dict["max_guest"])

    def test_update_valid_ydictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "update Place {} ".format(ytestId)
        ytestCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual(9.8, ytes_dict["latitude"])

    def test_update_valid_ydictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            HBNBCommand().onecmd("create Place")
            ytestId = youtput.getvalue().strip()
        ytestCmd = "Place.update({}, ".format(ytestId)
        ytestCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(ytestCmd)
        ytes_dict = storage.all()["Place.{}".format(ytestId)].__dict__
        self.assertEqual(9.8, ytes_dict["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests test count method HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def test_count_yinvalid_class(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", youtput.getvalue().strip())

    def test_count_yobject(self):
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", youtput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as youtput:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", youtput.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
