from flask import Flask, render_template, request
from requests import post
from os import getenv

from wrapper.user_wrapper import get_user
from wrapper.repo_wrapper import get_user_repos
from storage_engine import Storage_Json
from models import UserModel, RepoModel

CLIENT_ID = getenv('GH_BASIC_CLIENT_ID')
CLIENT_SECRET = getenv('GH_BASIC_SECRET_ID')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", client_id=CLIENT_ID)


@app.route("/callback")
def callback():
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

    if (user_id not in Storage_Json.all(UserModel.User)):
        user_info["user_etag"] = user_request.headers.get("etag")

        repo_request = get_user_repos(access_token, headers=header)
        user_info["repo_etag"] = repo_request["etag"]
        repo_objs = [RepoModel.Repo(**repo) for repo in repo_request["repos"]]
        
        new_user = UserModel.User(**user_info)
        new_user.save()

        new_user.save_repos(repo_objs)

    return "success"
    # return render_template("landing.html")

if __name__ == "__main__":
    app.run()
