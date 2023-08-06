# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class YubicoAPIForm(FlaskForm):
    client_id = IntegerField(description='Client ID',
                             validators=[DataRequired('Client ID is required and must be a number'),
                                         NumberRange(message='Number is required', min=None, max=999999)])
    secret_key = StringField(description='Secret Key',
                             validators=[DataRequired('Secret is required for API'),
                                         Length(message='Secret can not be longer than 40 characters', max=44)])
    submit_btn = SubmitField('Save Yubico')
