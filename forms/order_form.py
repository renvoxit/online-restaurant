from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class OrderForm(FlaskForm):
    address = StringField("Delivery Address", validators=[
                          DataRequired(), Length(max=200)])
    submit = SubmitField("Place Order")
