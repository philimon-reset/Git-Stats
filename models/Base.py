#!/usr/bin/python3
"""
    Module containing BaseModel
"""
from uuid import uuid4
from datetime import datetime
import models

class BaseModel():
    """
        Base class to define all common attributes and methods for
        other classes
    """
    def __init__(self, *args, **kwargs):
        """
            initialization
        """
        if kwargs:
            for key in kwargs:
                if key == "__class__":
                    continue
                elif key in ("created_at", "updated_at"):
                    iso = "%Y-%m-%dT%H:%M:%S.%f"
                    setattr(self, key, datetime.strptime(kwargs[key], iso))
                else:
                    setattr(self, key, kwargs[key])
        else:
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
            return string representation of a Model
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
            update latest updation time of a model
        """
        self.updated_at = datetime.now()
        if (self.__class__.__name__ == "User"):
            models.storage.new_user(self)
            models.storage.save_users()
        if (self.__class__.__name__ == "Repo"):
            models.storage.new_repo(self, self.user)
            models.storage.save_users()

    def to_dict(self):
        """
            custom representation of a model
        """
        custom_dict = {}
        custom_dict.update({"__class__": self.__class__.__name__})
        for key in self.__dict__:
            if key in ("created_at", "updated_at"):
                custom_dict.update({key: getattr(self, key).isoformat()})
            elif key == "_sa_instance_state":
                del self.__dict__[key]
            else:
                custom_dict.update({key: getattr(self, key)})
        return custom_dict

    def delete(self):
        """ delete the current instance from the storage
        """
        k = "{}.{}".format(type(self).__name__, self.id)
        del models.storage.__objects[k]
