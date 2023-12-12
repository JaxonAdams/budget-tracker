"""Connect to the MongoDB database."""

import os
from mongoengine import connect


def connect_to_db(env):
    """Given the current environment (DEV or PROD), connect to either
    a local MongoDB database or the production db hosted on Atlas.
    """

    if env.lower() == "prod":
        print("CONNECTING TO PRODUCTION DATABASE")
        return connect(host=f"mongodb+srv://JaxonAdams:{os.environ['DB_PW']}@cluster0.dw8oz.mongodb.net/?retryWrites=true&w=majority")
    elif env.lower() == "dev":
        print("CONNECTING TO LOCAL DATABASE")
        return connect("budget_tracker")
    else:
        raise ValueError(f"Invalid env value: {env}")
