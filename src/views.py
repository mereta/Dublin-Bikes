"""The views that will be rendered."""

from flask import render_template
# url_for function is not used in this file, but IS used in the html templates
from flask import url_for


from app import app


@app.route("/")
def index():
    return render_template("index.html")
