"""Model a User in the database."""

import mongoengine as me

class User(me.Document):
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    email = me.StringField(required=True)
    password = me.StringField(required=True)
