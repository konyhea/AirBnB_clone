import os
import unittest
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorageInit(unittest.TestCase):
    '''Testing the instantiation of FileStorage'''

    def test_FileStorage(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_init(self):
        self.assertEqual(type(storage), FileStorage)


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_file.json"
        FileStorage._FileStorage__file_path = self.test_file

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_all(self):
        self.assertEqual(dict, type(storage.all()))

    def test_new(self):
        test = BaseModel()
        storage.new(test)
        key = "BaseModel.{}".format(test.id)
        self.assertIn(key, storage.all())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        with self.assertRaises(AttributeError):
            storage.new(None)

    def test_save_and_reload(self):
        test1 = BaseModel()
        test2 = BaseModel()
        storage.new(test1)
        storage.new(test2)
        storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        self.assertTrue(
            new_storage.all().get("BaseModel.{}".format(test1.id)) is not None
        )
        self.assertTrue(
            new_storage.all().get("BaseModel.{}".format(test2.id)) is not None
        )

    def test_save_to_file(self):
        test = BaseModel()
        storage.new(test)
        storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_reload_empty_file(self):
        with open(FileStorage._FileStorage__file_path, 'w') as f:
            f.write("{}")
        storage.reload()
        self.assertEqual(storage.all(), {})


if __name__ == "__main__":
    unittest.main()
