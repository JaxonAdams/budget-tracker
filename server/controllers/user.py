"""Provide API routes for interacting with User documents."""

import bcrypt
import flask

import models.User as user_model


def find_user_by_email(email):
    """Get a user by the provided email address."""

    hits = user_model.User.objects(email=email)
    if len(hits) == 0:
        return {
            "error": "User not found.",
        }, 404

    if len(hits) > 1:
        return {
            "error": "Multiple users found. (not sure how we got here...)",
            "users": [{
                        "name": f"{hit['first_name']} {hit['last_name']}",
                        "email": hit["email"],
                      } for hit in hits],
        }, 500
    
    # return all values for user
    return hits[0]


def get_user(email):
    """Search for a user by email and return all data except for 
    their password.
    """
    
    # get all values
    user = find_user_by_email(email)

    # return all except password
    return { "User": user.except_pw() }, 200


def register_user(data):
    """Register a new user. Requires an email, password, and full name."""

    # search for existing user
    try:
        existing = user_model.User.objects(email=data["email"])[0]
    except IndexError:
        # user does not exist yet
        existing = None

    if existing is not None:
        return {
            "error": f"User with email {data['email']} already exists.",
        }

    # hash password
    hashed = bcrypt.hashpw(data["password"].encode("UTF-8"), 
                           bcrypt.gensalt()).decode("UTF-8")
    
    # add user to database
    new_user = user_model.User()
    new_user.first_name = data["first_name"]
    new_user.last_name = data["last_name"]
    new_user.email = data["email"]
    new_user.password = hashed
    new_user.save()

    return {
        "email": data["email"],
        "password": hashed,
        "success": True
    }, 200


def login_user(data):
    """Log a user in by checking their email and password."""

    # user may already be logged in
    if "email" in flask.session:
        return {
            "logged_in": True,
            "email": flask.session["email"],
        }, 200

    usr_pw = data["password"].encode("UTF-8")
    user = find_user_by_email(data["email"])
    
    # error included in find_user_by_email if user not found
    if "error" in user:
        return user
    
    hashed_pw = user["password"].encode("UTF-8")
    if hashed_pw == bcrypt.hashpw(usr_pw, hashed_pw):
        flask.session["email"] = user["email"]
        if "redirect" in data:
            return flask.redirect(data["redirect"])
        return {
            "logged_in": True,
            "email": flask.session["email"],
        }, 200
    
    # incorrect password
    return {
        "error": "Incorrect password."
    }


def logout_user():
    """Log the current user out by deleting their session info."""

    flask.session.pop("email", None)
    return {
        "logged_in": False,
    }, 200
