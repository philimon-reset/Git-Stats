""" Application server for the git stats project"""

from flask import Flask, render_template, request, send_from_directory, redirect, make_response
from requests import post
from flask_cors import CORS
from os import getenv
from uuid import uuid4
from wrapper.user_wrapper import get_user
from wrapper.repo_wrapper import get_user_repos
from storage_engine import Storage_Json
from models import UserModel, RepoModel

CLIENT_ID = getenv('GH_BASIC_CLIENT_ID')
CLIENT_SECRET = getenv('GH_BASIC_SECRET_ID')

app = Flask(__name__)
CORS(app)

# Routes
##########################################################################

@app.route('/')
def index():
    """ begining route where the project begins
    """
    return render_template("index.html", client_id=CLIENT_ID)


@app.route("/callback")
def callback():
    """ callback route sent after github authorization is completed"""
    session_code = request.args.get("code")
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": session_code
    }

    header = {
        "Accept": "application/vnd.github.v3+json"
    }

    git_response = post(
        "https://github.com/login/oauth/access_token",
        params=data,
        headers=header)

    access_token = git_response.json().get("access_token")

    user_request = get_user(access_token, headers=header)
    user_info = user_request.json()
    user_id = user_info.get("id")

    if (not Storage_Json.get_stored_user(user_id)):
        user_info["user_etag"] = user_request.headers.get("etag")
        user_info["access_token"] = access_token

        repo_request = get_user_repos(access_token, user_id, headers=header)
        user_info["repo_etag"] = repo_request["etag"]
        repo_objs = [RepoModel.Repo(**repo) for repo in repo_request["repos"]]

        new_user = UserModel.User(**user_info)
        new_user.save()

        new_user.save_repos(repo_objs)

    # return "success"
    # return render_template("landing.html", user=user_info)
    return redirect(f"/profile/{user_id}")


@app.route("/gitstat/<string:user_id>")
def get_template(user_id):
    """ build and return the template containing the account's information"""
    update_user(user_id)
    update_user_repos(user_id)
    user = Storage_Json.get_stored_user(user_id).to_dict()
    user_repos = [repo.to_dict()
                  for repo in Storage_Json.get_stored_user_repos(user_id)]
    return render_template(
        'user_template.html',
        cache_id=uuid4(),
        user_info=user,
        user_repo_info=user_repos)


## TODO proper referer identification
@app.route("/getembed", methods=["GET"])
def get_embed():
    """get embed script"""
    referer = request.headers.get("Referer")
    referer = referer[7:21]
    print(referer)
    response = make_response(send_from_directory("static", "embed.js"))
    response.set_cookie("GitStatUsr", Storage_Json.get_user_id_from_url(referer))
    return response

@app.route("/profile/<string:user_id>")
def profile(user_id):
    """
    profile page
    """
    user_info = Storage_Json.get_stored_user(user_id).to_dict()
    return render_template("landing.html", user=user_info)

@app.route("/register_url/<string:user_id>", methods=["POST"])
def register_url(user_id):
    """
    register a new site for a user
    """
    url = request.form.get("urlinput")
    Storage_Json.new_url(user_id, url)
    Storage_Json.save_userURLs()
    return redirect(f"/profile/{user_id}")

# Functions
##########################################################################

def update_user(user_id):
    """ update user info if the user is already in the database"""
    user = Storage_Json.get_stored_user(user_id)
    update = get_user(user.access_token, user.user_etag)
    if update:
        updated_user_info = update.json()
        updated_user_info["user_etag"] = update.headers.get("etag")
        user.update(**updated_user_info)
        user.save()


def update_user_repos(user_id):
    """ update the users repo if the repo is already in the database"""
    user = Storage_Json.get_stored_user(user_id)
    user_repos = Storage_Json.get_stored_user_repos(user_id)
    update = get_user_repos(user.access_token, user.id, etag=user.repo_etag)
    if update["repos"]:
        user.repo_etag = update["etag"]
        user.save()
        # hot fix
        for repo in update["repos"]:
            for old_repo in user_repos:
                if repo["id"] == old_repo.id:
                    old_repo.update(**repo)
        Storage_Json.save_repos()


##########################################################################
if __name__ == "__main__":
    """ run the flask instance"""
    app.run()
