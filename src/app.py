from flask import Flask

# Keep all the config in the config.py file, don't hardcode deployment details.
import config

# Flask likes to know the name of the script calling it.
app = Flask(__name__)

# Typically imports go at the top, however views.py imports app from here,
# so the import must come after the app assignment.
from views import *


if __name__ == "__main__":
    app.run(config=config.development_config)
