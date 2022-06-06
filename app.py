from flask import Flask, request
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
    return serve_template("index.html", host_url=request.host_url)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
