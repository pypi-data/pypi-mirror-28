# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, IPAddress


class SettingsNetworkForm(FlaskForm):
    """Network settings

    """
    host_name = StringField(description='Host Name',
                            validators=[DataRequired(message='Host name required')])
    dhcp_mode = BooleanField(description='IP Mode')
    ip_address = StringField(description='Lock IP',
                             validators=[DataRequired(message='IP Address required'),
                                         IPAddress(message='Must match IPV4 format')])
    sub_address = StringField(description='Subnet',
                              validators=[DataRequired(message='Subnet Address required'),
                                          IPAddress(message='Must match IPV4 format')])
    gw_address = StringField(description='Gateway',
                             validators=[DataRequired(message='Gateway Address required'),
                                         IPAddress(message='Must match IPV4 format')])
    dns1_address = StringField(description='DNS 1',
                               validators=[DataRequired(message='DNS Address required'),
                                           IPAddress(message='Must match IPV4 format')])
    dns2_address = StringField(description='DNS 2',
                               validators=[IPAddress(message='Must match IPV4 format')])
    submit_btn = SubmitField('Save Network')

    def validate(self):
        if self.dhcp_mode:
            return True
        else:
            return self.FlaskForm.validate(self)
