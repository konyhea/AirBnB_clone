#!/usr/bin/python3

''' testing the base models with unittest '''
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    ''' testing the base model '''
    def test_init(self):
        ''' testing the constructor '''
        model = BaseModel()
        self.assertIsNotNone(model.id)
        self.assertIsNotNone(model.created_at)
        self.assertIsNotNone(model.updated_at)

    def test_save(self):
        ''' test the save method '''
        model = BaseModel()
        initial_time = model.updated_at
        model.save()
        self.assertNotEqual(initial_time, model.updated_at)

    def test_dict(self):
        ''' testing the copy dict '''
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)

        self.assertEqual(
            model_dict["__class__"], model.__class__.__name__
        )
        self.assertEqual(model_dict["id"], model.id)
        self.assertEqual(
            model_dict["created_at"], model.created_at.isoformat()
        )
        self.assertEqual(
            model_dict["updated_at"], model.updated_at.isoformat()
        )

    def test_str(self):
        ''' test the str method '''
        model = BaseModel()
        self.assertTrue(str(model).startswith('[BaseModel]'))
        self.assertIn(model.id, str(model))
        self.assertIn(str(model.__dict__), str(model))


if __name__ == "__main__":
    unittest.main()
