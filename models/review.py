#!/usr/bin/python3
"""defines deview class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """represent revie.

    Attributes:
        place_id (str): the Place id.
        user_id (str): the User id.
        text (str): the text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
