from wtforms import (
    BooleanField,
    Form,
    HiddenField,
    PasswordField,
    StringField,
    validators,
)


class LoginForm(Form):
    username = StringField(
        "Username",
        [
            validators.DataRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
        ],
    )
    remember = BooleanField("Remember me", [validators.Optional()])
    next = HiddenField()
