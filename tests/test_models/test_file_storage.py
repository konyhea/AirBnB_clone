import os
import unittest
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorageInit(unittest.TestCase):
    '''Testing the instantiation of file storage.'''

    def test_FileStorage(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_init(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.test_file = "test_file.json"
        FileStorage._FileStorage__file_path = self.test_file
        models.storage.reload()

    def tearDown(self):
        """Tear down test environment."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_all(self):
        """Test the all method."""
        self.assertEqual(type(models.storage.all()), dict)

    def test_new(self):
        """Test the new method."""
        test = BaseModel()
        models.storage.new(test)
        self.assertIn("BaseModel.{}".format(test.id), models.storage.all())

    def test_new_with_args(self):
        """Test the new method with arguments."""
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        """Test the new method with None."""
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_and_reload(self):
        """Test save and reload methods."""
        test1 = BaseModel()
        test2 = BaseModel()
        models.storage.new(test1)
        models.storage.new(test2)
        models.storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        self.assertIsNotNone(
            new_storage.all().get("BaseModel.{}".format(test1.id))
        )
        self.assertIsNotNone(
            new_storage.all().get("BaseModel.{}".format(test2.id))
        )

    def test_save_to_file(self):
        """Test saving to file."""
        test = BaseModel()
        models.storage.new(test)
        models.storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_reload_empty_file(self):
        """Test reloading from an empty file."""
        with open(self.test_file, 'w') as f:
            f.write("{}")
        new_storage = FileStorage()
        new_storage.reload()
        self.assertEqual(new_storage.all(), {})


if __name__ == "__main__":
    unittest.main()
