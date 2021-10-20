from storage_engine import  Storage_Json


""" User object """
class User():
    def __init__(self, *args, **kwargs):
        self.id = 0
        self.login = ""
        self.name = ""
        self.gravatar_id = ""
        self.avatar_url = ""
        self.email = ""
        self.html_url = ""
        self.bio = ""
        self.twitter_username = ""
        self.public_repos = ""
        self.followers = ""
        self.following = ""
        if kwargs:
            for attr, val in kwargs:
                if hasattr(self, attr):
                    setattr(self, attr, val)

    def update(self, **kwargs):
        """ update user attributes """
        for attr, val in kwargs:
            if hasattr(self, attr):
                setattr(self, attr, val)

    def save(self):
        """ save user attributes in the storage
        """
        Storage_Json.new_user(self)
        Storage_Json.save_user()
