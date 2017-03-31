from flask import Flask, render_template, url_for


try:
    # when running locally...
    import config
except ImportError:
    # when installed and running from the command line...
    from . import config

# Flask likes to know the name of the script calling it.
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def main():
    app.config.from_object(config.DevelopmentConfig)
    app.run()

if __name__ == "__main__":
    main()
