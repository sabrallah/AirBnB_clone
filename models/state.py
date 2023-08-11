#!/usr/bin/python3
"""defines the state class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represent state.

    Attributes:
        name (str): The name the my only state.
    """

    name = ""
