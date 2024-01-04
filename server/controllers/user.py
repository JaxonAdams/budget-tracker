"""Provide API routes for interacting with User documents."""

import bcrypt
import models.User as user_model


def get_user(email):
    """Get a user by the provided email address."""

    hits = user_model.User.objects(email=email)
    if len(hits) == 0:
        return {
            "Error": "User not found."
        }, 404

    if len(hits) > 1:
        return {
            "Error": "Multiple users found. (not sure how we got here...)",
            "Users": [{
                        "name": f"{hit['first_name']} {hit['last_name']}",
                        "email": hit["email"],
                      } for hit in hits]
        }, 500
    
    # get all values except password
    user = hits[0].except_pw()

    return { "User": user }, 200


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
            "error": f"User with email {data['email']} already exists."
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
