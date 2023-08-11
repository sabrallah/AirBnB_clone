#!/usr/bin/python3
"""the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    ycurly_braces = re.search(r"\{(.*?)\}", arg)
    ybrackets = re.search(r"\[(.*?)\]", arg)
    if ycurly_braces is None:
        if ybrackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            ylexer = split(arg[:ybrackets.span()[0]])
            yretl = [i.strip(",") for i in ylexer]
            yretl.append(ybrackets.group())
            return yretl
    else:
        ylexer = split(arg[:ycurly_braces.span()[0]])
        yretl = [i.strip(",") for i in ylexer]
        yretl.append(ycurly_braces.group())
        return yretl


class HBNBCommand(cmd.Cmd):
    """Defines the alxbnb command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        yargdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        ymatch = re.search(r"\.", arg)
        if ymatch is not None:
            yargl = [arg[:ymatch.span()[0]], arg[ymatch.span()[1]:]]
            ymatch = re.search(r"\((.*?)\)", yargl[1])
            if ymatch is not None:
                ycommand = [yargl[1][:ymatch.span()[0]], ymatch.group()[1:-1]]
                if ycommand[0] in yargdict.keys():
                    ycall = "{} {}".format(yargl[0], ycommand[1])
                    return yargdict[ycommand[0]](ycall)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        yargl = parse(arg)
        if len(yargl) == 0:
            print("** class name missing **")
        elif yargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(yargl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        yargl = parse(arg)
        yobjdict = storage.all()
        if len(yargl) == 0:
            print("** class name missing **")
        elif yargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(yargl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(yargl[0], yargl[1]) not in yobjdict:
            print("** no instance found **")
        else:
            print(yobjdict["{}.{}".format(yargl[0], yargl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        yargl = parse(arg)
        yobjdict = storage.all()
        if len(yargl) == 0:
            print("** class name missing **")
        elif yargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(yargl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(yargl[0], yargl[1]) not in yobjdict.keys():
            print("** no instance found **")
        else:
            del yobjdict["{}.{}".format(yargl[0], yargl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        yargl = parse(arg)
        if len(yargl) > 0 and yargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            yobjl = []
            for obj in storage.all().values():
                if len(yargl) > 0 and yargl[0] == obj.__class__.__name__:
                    yobjl.append(obj.__str__())
                elif len(yargl) == 0:
                    yobjl.append(obj.__str__())
            print(yobjl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        yargl = parse(arg)
        ycount = 0
        for obj in storage.all().values():
            if yargl[0] == obj.__class__.__name__:
                ycount += 1
        print(ycount)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        yargl = parse(arg)
        yobjdict = storage.all()

        if len(yargl) == 0:
            print("** class name missing **")
            return False
        if yargl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(yargl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(yargl[0], yargl[1]) not in yobjdict.keys():
            print("** no instance found **")
            return False
        if len(yargl) == 2:
            print("** attribute name missing **")
            return False
        if len(yargl) == 3:
            try:
                type(eval(yargl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(yargl) == 4:
            obj = yobjdict["{}.{}".format(yargl[0], yargl[1])]
            if yargl[2] in obj.__class__.__dict__.keys():
                yvaltype = type(obj.__class__.__dict__[yargl[2]])
                obj.__dict__[yargl[2]] = yvaltype(yargl[3])
            else:
                obj.__dict__[yargl[2]] = yargl[3]
        elif type(eval(yargl[2])) == dict:
            obj = yobjdict["{}.{}".format(yargl[0], yargl[1])]
            for k, v in eval(yargl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    yvaltype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = yvaltype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
