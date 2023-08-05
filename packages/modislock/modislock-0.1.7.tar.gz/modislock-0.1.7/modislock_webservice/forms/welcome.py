# coding: utf-8

from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField, SelectField
from wtforms.validators import Email, InputRequired, Length, NumberRange, ValidationError
import re

# Existing form
from .timezone_settings import TimeZoneSettings


def email_validate(form, field):
    email_test = re.match("^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", form.email.data)
    if email_test is None:
        raise ValidationError(message='Enter a valid email address')


class WelcomeForm(TimeZoneSettings):

    serial_number = StringField(label='Serial Number', description='Serial Number', 
                                validators=[InputRequired(message='Enter a valid serial number')],
                                render_kw={"placeholder": "00000000"})
    first_name = StringField(label='First Name', description='First Name',
                             validators=[InputRequired(message='First Name Required'),
                                         Length(max=40)])
    last_name = StringField(label='Last Name', description='Last Name',
                            validators=[InputRequired(message='Last Name Required'),
                                        Length(max=40)])
    email = StringField(label='Email Address',
                        description='Administrator Email Address',
                        validators=[InputRequired(message='Email Required'),
                                    Length(max=60), email_validate])
    password = PasswordField(label='Admin Password', description='Administrator Password',
                             validators=[InputRequired(message='Password Required'),
                                         Length(max=20)])
    pwd_confirm = PasswordField(label='Password Confirm', description='Administrator Password Confirmation',
                                validators=[InputRequired(message='Password Required'),
                                            Length(max=20)])

    submit_btn = SubmitField(label='Submit Data', description='Submit Data')