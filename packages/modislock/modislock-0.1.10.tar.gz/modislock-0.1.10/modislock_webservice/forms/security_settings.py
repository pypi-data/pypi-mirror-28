# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField


class SecuritySettingsForm(FlaskForm):
    """Security settings are things that define how long data will be preserved, how many digits the PIN codes
    will have and what events does the administrator need to be notified.
    """
    # SelectField(default field arguments, choices=[], coerce=unicode, option_widget=None)
    months_preserved = SelectField(description='Data Preserve',
                                   choices=[('1', '1 Month'), ('2',  '2 Months'), ('3', '3 Months'), ('4', '4 Months')])
    pin_places = SelectField(description='Pin Length',
                             choices=[('4', '4 Places'), ('5', '5 Places'), ('6', '6 Places'), ('7', '7 Places')])
    notify_on_denied = BooleanField(description='Notify on Denied')
    notify_on_after_hours = BooleanField(description='Notify on After Hours')
    notify_on_system_error = BooleanField(description='Notify on System Error')

    submit_btn = SubmitField('Save Security')
