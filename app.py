from flask import Flask, request, flash, get_flashed_messages, redirect, url_for
from mako.lookup import TemplateLookup
from httpx import get
from json import loads

app = Flask(__name__)

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
    # If the user's JSON contains a message key, i.e. request has failed,
    # We will flash the error message back to the user
    # If it doesn't exist, we will display content as usual
    try:
        user_json["message"]
        flash(f"Error when requesting user: {user_json['message']}")
        return redirect(url_for("/"))
    except Exception as _:
        return serve_template("user.html", user=user_json, host_url=request.host_url)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
