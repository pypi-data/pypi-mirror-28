# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError


# def time_validate(form, field):
#     if form.glob_start_hour.data is not None:
#         if form.glob_start_min.data is not None:
#             if form.glob_stop_hour.data is not None:
#                 if form.glob_stop_min.data is not None:
#                     start_time = form.glob_start_hour.data * 60 + form.glob_start_min.data
#                     stop_time = form.glob_stop_hour.data * 60 + form.glob_stop_min.data
#
#                     if start_time >= stop_time:
#                         raise ValidationError(message="End time must be after Start time")
#
#
# def days_validate(form, field):
#     if form.glob_mon.data + form.glob_tue.data + form.glob_wed.data + form.glob_thr.data + \
#             form.glob_fri.data + form.glob_sat.data + form.glob_sun.data == 0:
#         raise ValidationError(message="Please select at least 1 day")


class GlobalTimeSettingsForm(FlaskForm):
    """Global access time rules

    """
    glob_start = StringField(description='Start Access Time')
    glob_end = StringField(description="End Access Time")

    # # Start hours
    # glob_start_hour = IntegerField(description='Start Access Hours',
    #                                validators=[InputRequired(message='Hour Required'),
    #                                            NumberRange(min=0, max=23, message='Hour=0..23')])
    # # End hours
    # glob_start_min = IntegerField(description='Start Access Minutes',
    #                               validators=[InputRequired(message='Minute Required'),
    #                                           NumberRange(min=0, max=59, message='Minute=0..59')])
    # # Start hours
    # glob_stop_hour = IntegerField(description='End Access Hours',
    #                               validators=[InputRequired(message='Hour Required'),
    #                                           NumberRange(min=0, max=23, message='Hour=0..23')])
    # # End hours
    # glob_stop_min = IntegerField(description='End Access Minutes',
    #                              validators=[InputRequired(message='Minute Required'),
    #                                          NumberRange(min=0, max=59, message='Minute=0..59')])
    # Days of week
    glob_mon = BooleanField(description='Mon')
    glob_tue = BooleanField(description='Tue')
    glob_wed = BooleanField(description='Wed')
    glob_thr = BooleanField(description='Thr')
    glob_fri = BooleanField(description='Fri')
    glob_sat = BooleanField(description='Sat')
    glob_sun = BooleanField(description='Sun')

    # Submit to save
    submit_btn = SubmitField('Save Rules')

    # def validate(self):
    #     valid = FlaskForm.validate(self)
    #
    #     if not valid:
    #         return False
    #
    #     start_time = self.glob_start_hour.data * 60 + self.glob_start_min.data
    #     stop_time = self.glob_stop_hour.data * 60 + self.glob_stop_min.data
    #
    #     if start_time >= stop_time:
    #         self.submit_btn.errors.append("End Time Must Be After Start time")
    #         return False
    #     else:
    #         return True
