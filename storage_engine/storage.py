#!/usr/bin/python3
"""
module containing FileStorage used for file storage
"""
import json

from requests.sessions import extract_cookies_to_jar
import models.UserModel as UserModel
import models.RepoModel as RepoModel

dummy_classes = {"User": UserModel.User, "Repo": RepoModel.Repo}

class FileStorage:
    """
    serializes and deserializes instances to and from JSON file
    saved into file_path

    """

    __file_repo = "repo.json"
    __file_user = "user.json"
    __users = {}
    __repos = {}


    def all(self, cls=None):
        """returns a dictionary containing every object"""
        if (cls == None):
            return {"users": self.__users, "repos": self.__repos}
        if (cls == dummy_classes["User"]):
            return self.__users
        if (cls == dummy_classes["Repo"]):
            return self.__repos

    def new_user(self, user):
        """
        creates a new object and saves it to __objects
        """
        self.__users[user.id] = user

    def new_repo(self, repo, user_id):
        """ add an instance to the repo dictionary """
        if not (self.__repos.get(user_id)):
            self.__repos[user_id] = []
        self.__repos[user_id].append(repo)

    def save_user(self):
        """
        update the JSON file to reflect any change in the users
        """
        temp = {}
        for id, obj in self.__users.items():
            temp[id] = obj.to_dict()
        with open(self.__file_user, "w") as json_file:
            json.dump(temp, json_file)

    def save_repos(self):
        """
        update the JSON file to reflect any change in the repos
        """
        temp = {}
        for id, obj in self.__repos.items():
            temp_list = []
            for repo in obj:
                temp_list.append(repo.to_dict())
            temp[id] = temp_list

        with open(self.__file_repo, "w") as json_file:
            json.dump(temp, json_file)

    def reload(self):
        """
        update users and repos dict to restore previously created pbjects
        """
        try:
            with open(self.__file_user, "r") as user_file:
                user_T = json.load(user_file)
            for id, user_obj in user_T.items():
                self.__users[int(id)] = dummy_classes["User"](**user_obj)
        except:
            pass
        try:
            with open(self.__file_repo, "r") as repo_file:
                repo_T = json.load(repo_file)
            for id, repos in repo_T.items():
                temp_repos = []
                for repo in repos:
                    temp_repos.append(dummy_classes["Repo"](**repo))
                self.__repos[int(id)] = temp_repos
        except Exception as e:
            print(e)

    def delete_repo(self, repo, user):
        """ to delete obj from __objects if it’s inside
        """
        self.__repos[user.id].remove(repo)

    def delete_user(self, user):
        """ to delete obj from __objects if it’s inside
        """
        del self.__users[user.id]
        del self.__repos[user.id]

    def get_stored_user(self, id):
        """ Get information on an instance of a user
        """
        return self.__users.get(int(id))

    def get_stored_user_repos(self, id):
        """ Get information on an instance of a repo
        """
        return self.__repos.get(int(id))
