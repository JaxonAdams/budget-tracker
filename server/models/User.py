"""Model a User in the database."""

import mongoengine as me

class User(me.Document):
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    email = me.StringField(required=True)
    password = me.StringField(required=True)

    def except_pw(self):
        """Return all values except the user's password."""

        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
