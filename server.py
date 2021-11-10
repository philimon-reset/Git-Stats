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
    return render_template("landing.html", user=user_info)

@app.route("/gitstat/<string:user_id>")
def get_template(user_id):
    update_user(user_id)
    update_user_repos(user_id)
    user = Storage_Json.get_stored_user(user_id).to_dict()
    user_repos = [repo.to_dict() for repo in Storage_Json.get_stored_user_repos(user_id)]
    return render_template('user_template.html', user_info=user, user_repo_info=user_repos)


def update_user(user_id):
    user = Storage_Json.get_stored_user(user_id)
    update = get_user(user.access_token, user.user_etag)
    if update:
        updated_user_info = update.json()
        updated_user_info["user_etag"] = update.headers.get("etag")
        user.update(**updated_user_info)
        user.save()

def update_user_repos(user_id):
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
                    old_repo.save()
        

if __name__ == "__main__":
    app.run()
