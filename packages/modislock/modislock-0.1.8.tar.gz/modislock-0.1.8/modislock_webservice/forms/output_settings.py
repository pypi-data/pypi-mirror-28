# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class OutputSettingsForm(FlaskForm):
    """Output settings related to physical relays

    Mechanical relays are capable of heavy currents and are paired with a smaller current solidstate relay.

    Each relay also has a delay time associated with it. This is the time the relay will remain activated.
    """
    relay_1_enabled = BooleanField(description='Relay 1 Enabled')
    relay_2_enabled = BooleanField(description='Relay 2 Enabled')
    output_1 = BooleanField(description='Output 1')
    output_2 = BooleanField(description='Output 2')
    relay_1_delay = IntegerField(description='Operation Delay', validators=[DataRequired()])
    relay_2_delay = IntegerField(description='Operation Delay', validators=[DataRequired()])
    submit_btn = SubmitField('Save Outputs')
