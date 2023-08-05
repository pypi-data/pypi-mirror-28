# coding: utf-8

# Flask
from flask import render_template, Blueprint, request, jsonify, current_app
from flask_security import login_required
from ..forms import SecuritySettingsForm, EmailSettingsForm

# Email
from modislock_webservice.extensions import mail
from modislock_webservice.utils.mail_utils import send_email

# Database
from ..models import SettingsValues, Settings, User, db
from sqlalchemy import or_
from sqlalchemy.exc import InternalError, IntegrityError


bp = Blueprint('settings_security', __name__)


def _save_email_settings(form):
    """Saves email settings to database and re-initializes the application dictionary

    :param form form:
    """
    old_settings = _get_email_settings()
    keys = set(old_settings.keys())
    result = True

    new_settings = dict()
    new_settings[form.mail_server.short_name.upper()] = form.mail_server.data
    new_settings[form.mail_port.short_name.upper()] = form.mail_port.data
    new_settings[form.mail_username.short_name.upper()] = form.mail_username.data
    new_settings[form.mail_password.short_name.upper()] = form.mail_password.data
    new_settings[form.mail_sender.short_name.upper()] = form.mail_sender.data
    new_settings[form.mail_use_tls.short_name.upper()] = form.mail_use_tls.data
    new_settings[form.mail_use_ssl.short_name.upper()] = form.mail_use_ssl.data

    for key in keys:
        if old_settings[key] != new_settings[key]:
            email = SettingsValues.query.filter(SettingsValues.settings_id_settings == Settings.query
                                                .with_entities(Settings.id_settings)
                                                .filter_by(settings_name=key).first()[0]) \
                .first()
            if 'USE' in key and 'USER' not in key:
                email.value = 'ENABLED' if new_settings[key] is True else 'DISABLED'
            elif 'PORT' in key:
                email.value = str(new_settings[key])
            else:
                email.value = new_settings[key]

            try:
                db.session.commit()
            except (IntegrityError, InternalError) as e:
                db.session.rollback()
                current_app.logger.error('Database error occurred in: {}'.format(e.args[2]))
                result = False

    _mail_settings = Settings.query \
        .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
        .filter(Settings.settings_name.like('MAIL%')) \
        .with_entities(Settings.settings_name, SettingsValues.value) \
        .all()

    mail_settings = dict()

    for record in _mail_settings:
        try:
            if record.value == 'ENABLED' or record.value == 'DISABLED':
                value = True if record.value == 'ENABLED' else False
            else:
                value = record.value

            mail_settings[record.settings_name] = value
        except KeyError:
            continue

    # Mail support
    if len(mail_settings) > 0:
        current_app.config['MAIL_SERVER'] = mail_settings.get('MAIL_SERVER', '')
        current_app.config['MAIL_PORT'] = int(mail_settings.get('MAIL_PORT', 0))
        current_app.config['MAIL_USE_TLS'] = mail_settings.get('MAIL_USE_TLS', False)
        current_app.config['MAIL_USE_SSL'] = mail_settings.get('MAIL_USE_SSL', False)
        current_app.config['MAIL_USERNAME'] = mail_settings.get('MAIL_USERNAME', '')
        current_app.config['MAIL_PASSWORD'] = mail_settings.get('MAIL_PASSWORD', '')
        current_app.config['MAIL_DEFAULT_SENDER'] = mail_settings.get('MAIL_SENDER', '')

    mail.init_app(current_app)

    return result


def _get_email_settings():
    """Retrieves email settings from database

    :return dict email:
    """
    email = dict()

    _email = Settings.query \
        .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
        .filter(Settings.settings_name.like('MAIL%')) \
        .with_entities(Settings.settings_name, Settings.units, SettingsValues.value) \
        .all()

    for setting in _email:
        name = setting[0]

        if setting[1] == 'boolean':
            value = True if setting[2] == 'ENABLED' else False
        elif setting[1] == 'integer':
            value = int(setting[2])
        elif setting[1] == 'float':
            value = float(setting[2])
        else:
            value = setting[2]

        email[name] = value

    return email


def _save_security_settings(form):
    """Saves various security settings to database

    :param form form:
    """
    old_records = _get_security_settings()
    keys = set(old_records.keys())
    new_settings = dict()
    result = True

    new_settings[form.pin_places.short_name.upper()] = form.pin_places.data
    new_settings[form.months_preserved.short_name.upper()] = form.months_preserved.data
    new_settings[form.notify_on_denied.short_name.upper()] = form.notify_on_denied.data
    new_settings[form.notify_on_after_hours.short_name.upper()] = form.notify_on_after_hours.data
    new_settings[form.notify_on_system_error.short_name.upper()] = form.notify_on_system_error.data

    for key in keys:
        try:
            if old_records[key] != new_settings[key]:
                record = Settings.query\
                    .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings)\
                    .filter(Settings.settings_name == key).first()

                if record.units == 'boolean':
                    value = 'ENABLED' if new_settings[key] is True else 'DISABLED'
                else:
                    value = new_settings[key]

                record = SettingsValues.query.filter(SettingsValues.settings_id_settings == record.id_settings).first()
                record.value = value

                try:
                    db.session.commit()
                except (IntegrityError, InternalError) as e:
                    db.session.rollback()
                    current_app.logger.error('Database error occurred in: {}'.format(e.args[2]))
                    result = False
        except KeyError:
            continue

    return result


def _get_security_settings():
    """Retrieves the security settings from database

    :return dict secure_settings:
    """
    records = Settings.query.join(SettingsValues) \
        .with_entities(Settings.settings_name, Settings.units, SettingsValues.value) \
        .filter(or_(Settings.settings_name == 'PIN_PLACES',
                    Settings.settings_name == 'MONTHS_PRESERVED',
                    Settings.settings_name.like('NOTIFY%'))).all()

    secure_settings = dict()

    for record in records:
        if record.units == 'boolean':
            value = True if record.value == 'ENABLED' else False
        elif record.units == 'integer':
            value = int(record.value)
        elif record.units == 'float':
            value = float(record.value)
        else:
            value = 0

        secure_settings[record.settings_name] = value

    return secure_settings


@bp.route('/settings/security', methods=['GET', 'POST'])
@login_required
def security_settings():
    """Route to security settings

    :return html settings_security.html:
    """
    security = SecuritySettingsForm()
    email = EmailSettingsForm()
    save_result = False

    if request.method == 'POST':
        form = request.form.get('submit_btn', None)

        if form is not None:
            if 'Security' in form:
                if security.validate():
                    save_result = _save_security_settings(security)
            elif 'Email' in form:
                if email.validate():
                    save_result = _save_email_settings(email)
    if request.is_xhr:
        recipients = User.query.with_entities(User.email).filter_by(id=1).one_or_none()
        # Send test email
        send_email(recipients.email, subject='Test Email from Modis Lock', template='test_email')
        return jsonify({'success': 'Sent email'}), 200
    try:
        settings = _get_security_settings()
    except ValueError as e:
        current_app.logger.error(e)
    else:
        security.pin_places.data = str(settings.get('PIN_PLACES', 1))
        security.months_preserved.data = str(settings.get('MONTHS_PRESERVED', 4))
        security.notify_on_after_hours.data = settings.get('NOTIFY_ON_AFTER_HOURS', False)
        security.notify_on_denied.data = settings.get('NOTIFY_ON_DENIED', False)
        security.notify_on_system_error.data = settings.get('NOTIFY_ON_SYSTEM_ERROR', False)

    # Email Settings
    try:
        settings = _get_email_settings()
    except Exception as e:
        current_app.logger.error(e)
    else:
        email.mail_server.data = settings.get('MAIL_SERVER', '')
        email.mail_port.data = settings.get('MAIL_PORT', 0)
        email.mail_username.data = settings.get('MAIL_USERNAME', '')
        email.mail_password.data = settings.get('MAIL_PASSWORD', '')
        email.mail_use_ssl.data = settings.get('MAIL_USE_SSL', False)
        email.mail_use_tls.data = settings.get('MAIL_USE_TLS', False)
        email.mail_sender.data = settings.get('MAIL_SENDER', '')

    return render_template('settings_security/settings_security.html', email_form=email, security_form=security,
                           save_result=save_result)
