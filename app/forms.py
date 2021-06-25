from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class UserAddressForm(FlaskForm):
    ICX_wallet_address = StringField(
        label='ICX Address:', validators=[Length(min=42, max=42, message="Not a valid ICX address"), DataRequired()])
    submit = SubmitField(label="let's go")
