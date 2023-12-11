"""Connect to the MongoDB database."""

from mongoengine import connect


def connect_to_db(env):
    """Given the current environment (DEV or PROD), connect to either
    a local MongoDB database or the production db hosted on Atlas.
    """

    if env.lower() == "prod":
        pass # TODO: IMPLEMENT ME
    elif env.lower() == "dev":
        return connect("budget_tracker")
    else:
        raise ValueError(f"Invalid env value: {env}")
