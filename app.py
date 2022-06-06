from flask import Flask
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
    return serve_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
