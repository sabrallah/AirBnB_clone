#!/usr/bin/python3
"""
contiens the TestReviewDocs classes
"""

from datetime import datetime
import inspect
from models import review
from models.base_model import BaseModel
import pep8
import unittest
Review = review.Review


class TestRevistionDocs(unittest.TestCase):
    """Tests pour verifier la documentation et le style de revis class"""
    @classmethod
    def setUpClass(cls):
        """Set up pour doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_review(self):
        """Test ce models/review.py conforme au PEP8."""
        pep = pep8.StyleGuide(quiet=True)
        resul = pep.check_files(['models/review.py'])
        self.assertEqual(resul.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_review(self):
        """Test ce tests/test_models/test_review.py conforme to PEP8."""
        pep = pep8.StyleGuide(quiet=True)
        resul = pep.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(resul.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_docstring(self):
        """Test le review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_class_docstring(self):
        """Test le the Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_func_docstrings(self):
        """Test pour le presence des docstrings dans Review methods"""
        for fun in self.review_f:
            self.assertIsNot(fun[1].__doc__, None,
                             "{:s} method needs a docstring".format(fun[0]))
            self.assertTrue(len(fun[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(fun[0]))


class TestReview(unittest.TestCase):
    """Test le Review class"""
    def test_subclass(self):
        """Test si Review est un subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id(self):
        """Test Review has attr place_id, et ses empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        self.assertEqual(review.place_id, "")

    def test_user_id(self):
        """Test Review has attr user_id, est ses empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        self.assertEqual(review.user_id, "")

    def test_text(self):
        """Test Review has attr text, and c'est une empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        self.assertEqual(review.text, "")

    def test_to_dict_creates(self):
        """test to_dict method creates a dictionary avec proper attrs"""
        y = Review()
        ne_d = y.to_dict()
        self.assertEqual(type(ne_d), dict)
        for attr in y.__dict__:
            self.assertTrue(attr in ne_d)
            self.assertTrue("__class__" in ne_d)

    def test_to_dict(self):
        """test that values in dict returned depuis to_dict are correct"""
        t_forma = "%Y-%m-%dT%H:%M:%S.%f"
        y = Review()
        ne_d = y.to_dict()
        self.assertEqual(ne_d["__class__"], "Review")
        self.assertEqual(type(ne_d["created_at"]), str)
        self.assertEqual(type(ne_d["updated_at"]), str)
        self.assertEqual(ne_d["created_at"], y.created_at.strftime(t_forma))
        self.assertEqual(ne_d["updated_at"], y.updated_at.strftime(t_forma))

    def test_str(self):
        """test that the str method a la correct output"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))
