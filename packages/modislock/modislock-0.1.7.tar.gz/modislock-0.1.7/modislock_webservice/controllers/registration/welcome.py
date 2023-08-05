# coding: utf-8

#Flask
from flask import render_template, Blueprint, request, current_app

# Subprocessing for restarting supervisor
from modislock_webservice.tasks import send_async_command

# Form
from forms.welcome import WelcomeForm

# Security
from flask_security.utils import hash_password

# Database
from models import db, User, Settings, SettingsValues

# Date time
from tzlocal import get_localzone

bp = Blueprint('welcome', __name__)


def save_reg_data(form):

    user = User.query.filter_by(id=1).one_or_none()

    # Admin User
    if user is not None:
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.password = hash_password(form.password.data)
        db.session.commit()

    # Serial Number
    serial = Settings.query.filter(Settings.settings_name == 'SERIAL_NUMBER').one_or_none()
    registration = Settings.query.filter(Settings.settings_name == 'REGISTRATION').one_or_none()

    if serial is not None:
        serial_num = SettingsValues.query\
            .filter(SettingsValues.settings_id_settings == serial.id_settings)\
            .one_or_none()
        if serial_num is not None:
            serial_num.value = form.serial_number.data
            db.session.commit()

    if registration is not None:
        reg_num = SettingsValues.query.filter(SettingsValues.settings_id_settings == registration.id_settings).one_or_none()

        if reg_num is not None:
            reg_num.value = 'DISABLED'
            db.session.commit()

    # Timezone and Time
    tzone = form.tz_zone.data
    hours = form.hours.data
    minutes = form.minutes.data

    if get_localzone().zone != tzone:
        args = ['timedatectl', 'set-timezone', tzone]
        send_async_command.delay(args)

    args = ['timedatectl', 'set-time', str(hours) + ':' + str(minutes) + ':00']
    send_async_command.delay(args)

    return True


@bp.route('/', methods=['GET', 'POST'])
def welcome():
    """Registration Page

    Controls the initial registration window(s).
    1. Serial Number
    2. Admin email address
    3. Admin password
    4. System Time Date Timezone
    5. Timezone

    :returns html_template welcome.html:
    """
    form = WelcomeForm()

    if request.method == 'POST':
        if form.validate():
            if save_reg_data(form):
                args = ['supervisorctl', 'restart', 'admin:modis_admin']
                send_async_command.delay(args)
                return render_template('welcome/birthing_new_lock.html', domain=current_app.config.get('SITE_DOMAIN'))
        else:
            current_app.logger.error('Could not validate registration form')

    form.tz_zone.data = get_localzone().zone

    return render_template('welcome/welcome.html', form=form)
