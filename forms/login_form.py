from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=5, max=128)])
