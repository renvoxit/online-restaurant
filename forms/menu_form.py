from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange


class MenuForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[
                                DataRequired(), Length(max=500)])
    description = StringField("Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[
                       DataRequired(), NumberRange(min=0)])
    image_url = StringField("Image URL", validators=[Length(max=255)])
