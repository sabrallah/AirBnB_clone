#!/usr/bin/python3
"""Defines BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs attributes.
        """
        ytform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = (str(uuid4()))
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for y, s in kwargs.items():
                if y == "created_at" or y == "updated_at":
                    self.__dict__[y] = datetime.strptime(s, ytform)
                else:
                    self.__dict__[y] = s
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at with current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name the object.
        """
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        return rdict

    def __str__(self):
        """Return the print/str representation of BaseModel instance."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
