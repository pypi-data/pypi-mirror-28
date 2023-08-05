# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class ReaderSettingsForm(FlaskForm):
    # Reader 1
    reader1 = StringField(description='Reader 1 Name',
                          validators=[DataRequired('Name Required'),
                                      Length(min=5, max=20, message='Name should be between 5 and 20 characters')])
    reader1_dir = BooleanField(description='Direction')
    reader1_relay = BooleanField(description='Door Relay')
    # Reader 2
    reader2 = StringField(description='Reader 2 Name',
                          validators=[DataRequired('Name Required'),
                                      Length(min=5, max=20, message='Name should be between 5 and 20 characters')])
    reader2_dir = BooleanField(description='Direction')
    reader2_relay = BooleanField(description='Door Relay')
    # Reader 3
    reader3 = StringField(description='Reader 3 Name',
                          validators=[DataRequired('Name Required'),
                                      Length(min=5, max=20, message='Name should be between 5 and 20 characters')])
    reader3_dir = BooleanField(description='Direction')
    reader3_relay = BooleanField(description='Door Relay')
    # Reader 4
    reader4 = StringField(description='Reader 4 Name',
                          validators=[DataRequired('Name Required'),
                                      Length(min=5, max=20, message='Name should be between 5 and 20 characters')])
    reader4_dir = BooleanField(description='Direction')
    reader4_relay = BooleanField(description='Door Relay')
    # Submit
    submit_btn = SubmitField('Save Reader')
