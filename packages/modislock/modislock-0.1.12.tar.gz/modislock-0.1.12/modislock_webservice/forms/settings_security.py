# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SettingsSecurityForm(FlaskForm):
    field = StringField('', validators=[DataRequired()])
