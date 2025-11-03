from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[
                        DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=5, max=128)])
