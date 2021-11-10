import storage_engine

""" User object """
class User():
    def __init__(self, *args, **kwargs):
        """ Initialize the user object
        """
        self.access_token = ""
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
        self.user_etag = ""
        self.repo_etag = ""
        if kwargs:
            for attr, val in kwargs.items():
                if hasattr(self, attr):
                    setattr(self, attr, val)

    def update(self, *args, **kwargs):
        """ update user attributes """
        for attr, val in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, val)

    def save(self):
        """ save user attributes in the storage
        """
        storage_engine.Storage_Json.new_user(self)
        storage_engine.Storage_Json.save_user()

    def save_repos(self, repos=[]):
        """ save repo objects related to a user
        """
        for x in repos:
            storage_engine.Storage_Json.new_repo(x, self.id)
        storage_engine.Storage_Json.save_repos()

    
    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        # new_dict["__class__"] = self.__class__.__name__
        return new_dict
