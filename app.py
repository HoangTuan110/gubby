from flask import Flask, request, flash, get_flashed_messages, redirect, url_for
from mako.lookup import TemplateLookup
from httpx import get
from json import loads

app = Flask(__name__)
app.config["SECRET_KEY"] = "265ceaf4cf562ec49f3ad1b187eaa84946b4e2b3090548a3d028a4a3c3a86322"

templates = TemplateLookup(directories=["./templates"], module_directory="/tmp/mako_modules")
def serve_template(name, **kwargs):
    template = templates.get_template(name)
    return template.render(**kwargs)

@app.route("/")
def index():
    return serve_template("index.html", host_url=request.host_url, messages=get_flashed_messages())

@app.route("/<user>")
def get_user(user):
    user_json = loads(get(f"https://api.github.com/users/{user}").text)
    # If the user's JSON doesn't contain a `login` key, i.e. request has failed,
    # We will flash the error message back to the user
    # If it does exist, we will render content as usual
    try:
        _ = user_json["login"]
        return serve_template("user.html", user=user_json)
    except KeyError:
        flash(f"Error when requesting user: {user_json['message']}")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
