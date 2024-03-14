from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# form used in basket
class CheckoutForm(FlaskForm):
    first_name = StringField("First Name", validators = [InputRequired()])
    surname = StringField("Surname", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired(), email()])
    phone = StringField("Phone Number", validators = [InputRequired()])
    address = StringField("Shipping Address", validators = [InputRequired()])
    submit = SubmitField("Checkout Order")