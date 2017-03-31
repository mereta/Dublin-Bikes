from flask import Flask, render_template, url_for

# Flask likes to know the name of the script calling it.
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
