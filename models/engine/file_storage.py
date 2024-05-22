import json
import os

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        with open(self.__file_path, 'w') as f:
            json.dump({key: obj.to_dict() for key, obj in self.__objects.items()}, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                objs = json.load(f)
                for key, val in objs.items():
                    cls_name = val['__class__']
                    cls = self.get_class(cls_name)
                    if cls:
                        self.__objects[key] = cls(**val)

    def get_class(self, class_name):
        """Dynamically imports and returns the class based on the class name."""
        if class_name == "BaseModel":
            from models.base_model import BaseModel
            return BaseModel
        elif class_name == "User":
            from models.user import User
            return User
        return None
