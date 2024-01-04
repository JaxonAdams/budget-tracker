"""Serve files and routes for the app."""

import os
from flask import Flask, request

import controllers.user
from db.connect import connect_to_db


app = Flask(__name__)
db = connect_to_db(os.environ["APP_ENV"])


@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"

@app.route("/api/users/<email>", methods=["GET"])
def get_user(email):
    """Get a user by the specified email address."""

    return controllers.user.get_user(email)

@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user, with an email and hashed password."""

    error = None
    if request.method == "POST":
        for required in ["email", "password", "first_name", "last_name"]:
            if required not in request.json:
                error = f"Field {required} is required."
                return error, 409
            
        return controllers.user.register_user(request.json)
