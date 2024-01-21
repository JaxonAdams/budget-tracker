"""Serve files and routes for the app."""

import os
from flask import Flask, request, session

import controllers.user
from db.connect import connect_to_db


app = Flask(__name__)
app.secret_key = os.environ["APP_SECRET"].encode("UTF-8")
db = connect_to_db(os.environ["APP_ENV"])


@app.route("/")
def index():
    if "email" in session:
        return f"<h1>Logged in -- hello {session['email']}!</h1>"
    return "<h1>Not currently logged in.</h1>"


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
    

@app.route("/api/login", methods=["POST"])
def login():
    """Log a user in by the provided email and password."""

    error = None
    if request.method == "POST":
        for required in ["email", "password"]:
            if required not in request.json:
                error = f"Field {required} is required."
                return error, 409
            
        return controllers.user.login_user(request.json)


@app.route("/api/logout", methods=["POST"])
def logout():
    """Log out a user."""

    if request.method == "POST":
        return controllers.user.logout_user()
