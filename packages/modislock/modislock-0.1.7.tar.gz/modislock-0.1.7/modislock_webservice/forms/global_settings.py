# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError


def time_validate(form, field):
    if form.glob_start_hour.data is not None:
        if form.glob_start_min.data is not None:
            if form.glob_stop_hour.data is not None:
                if form.glob_stop_min.data is not None:
                    start_time = form.glob_start_hour.data * 60 + form.glob_start_min.data
                    stop_time = form.glob_stop_hour.data * 60 + form.glob_stop_min.data

                    if start_time >= stop_time:
                        raise ValidationError(message="End time must be after Start time")


def days_validate(form, field):
    if form.glob_mon.data + form.glob_tue.data + form.glob_wed.data + form.glob_thr.data + \
            form.glob_fri.data + form.glob_sat.data + form.glob_sun.data == 0:
        raise ValidationError(message="Please select at least 1 day")


class GlobalTimeSettingsForm(FlaskForm):
    # field = StringField(description='days', validators=[DataRequired()])
    glob_start_hour = IntegerField(label='Access Hours', description='Start at',
                                   validators=[InputRequired(message='Hour Required'),
                                               NumberRange(min=0, max=23, message='Hour=0..23')])
    glob_start_min = IntegerField(validators=[InputRequired(message='Minute Required'),
                                              NumberRange(min=0, max=59, message='Minute=0..59')])
    glob_stop_hour = IntegerField(description='End at',
                                  validators=[InputRequired(message='Hour Required'),
                                              NumberRange(min=0, max=23, message='Hour=0..23')])
    glob_stop_min = IntegerField(
        validators=[InputRequired(message='Minute Required'),
                    NumberRange(min=0, max=59, message='Minute=0..59'),
                    time_validate])

    glob_mon = BooleanField(description='Monday')
    glob_tue = BooleanField(description='Tueday')
    glob_wed = BooleanField(description='Wednesday')
    glob_thr = BooleanField(description='Thursday')
    glob_fri = BooleanField(description='Friday')
    glob_sat = BooleanField(description='Saturday')
    glob_sun = BooleanField(description='Sunday', validators=[days_validate])

    submit_btn = SubmitField('Save Rules')
