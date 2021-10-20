from flask import Flask, render_template, request
from requests import post
from os import getenv
from storage_engine import storage_json

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

    user_info = get_user(access_token, None).json()
    trim(user_info)
    user_id = user_info.get("id")

    if (user_id in storage.all(cls=User)):
        usr = storage.all(cls=User)[user_id]
        usr.update(**user_info)
        usr.save()
    else:''
        new_user = User(**user_info)
        new_user.save()
    return "success"
    # return render_template("landing.html")

if __name__ == "__main__":
    app.run()
