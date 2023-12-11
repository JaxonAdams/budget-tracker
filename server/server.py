"""Serve files and routes for the app."""

import os
from flask import Flask

from db.connect import connect_to_db


app = Flask(__name__)
db = connect_to_db(os.environ["APP_ENV"])


@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"
