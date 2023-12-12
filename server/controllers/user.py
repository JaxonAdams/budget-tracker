"""Provide API routes for interacting with User documents."""

import bcrypt
import models.User as user_model


def register_user(data):
    """Register a new user. Requires an email, password, and full name."""

    # search for existing user
    try:
        existing = user_model.User.objects(email=data["email"])[0]
    except IndexError:
        # user does not exist yet
        existing = None

    if existing is not None:
        return {"error": f"User with email {data['email']} already exists."}
    
    # hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(data["password"].encode("UTF-8"), salt).decode("UTF-8")

    return {
        "email": data["email"],
        "password": hashed,
        "success": True
    }, 200
