import json
import re

from wtforms import (
    BooleanField,
    Field,
    Form,
    PasswordField,
    RadioField,
    StringField,
    validators,
)
from wtforms.validators import URL, Email, Regexp, ValidationError


class UserRegistrationForm(Form):
    username = StringField(
        "Username",
        [
            validators.DataRequired(),
            validators.Length(min=4, max=25),
            validators.Regexp("[0-9A-Za-z_]+"),
        ],
    )
    display_name = StringField("Display Name", [validators.Length(min=0, max=35)])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("password_again", message="Passwords must match"),
        ],
    )
    password_again = PasswordField("Repeat Password")
    is_admin = RadioField(
        "Privileges",
        [
            validators.InputRequired(),
        ],
        choices=["0", "1"],
    )


class UserEditForm(Form):
    """
    Form for already registered users
    """

    display_name = StringField("Display Name", [validators.Length(min=0, max=35)])
    password = PasswordField(
        "Password",
        [
            validators.EqualTo("password_again", message="Passwords must match"),
        ],
    )
    password_again = PasswordField("Repeat Password")
    is_admin = RadioField(
        "Privileges",
        [
            validators.InputRequired(),
        ],
        choices=["0", "1"],
    )
