# coding: utf-8

# Flask
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from flask_security import login_required
from modislock_webservice.forms import GlobalTimeSettingsForm

# Database
from modislock_webservice.models import db, SettingsValues, Settings
from sqlalchemy.exc import InternalError, IntegrityError


bp = Blueprint('settings_rules', __name__)


def _save_glob_rules_settings(form):
    """Saves various global rule(s) settings to database

    :param form form:
    """

    old_settings = _get_glob_rules_settings()
    keys = set(old_settings.keys())
    result = True

    new_settings = dict()
    new_settings['GLOBAL_DAYS'] = 0b00000001 if form.glob_mon.data == 1 else 0b00000000
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 1) if form.glob_tue.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 1)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 2) if form.glob_wed.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 2)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 3) if form.glob_thr.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 3)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 4) if form.glob_fri.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 4)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 5) if form.glob_sat.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 5)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 6) if form.glob_sun.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 6)
    new_settings['GLOBAL_START_TIME'] = form.glob_start.data
    new_settings['GLOBAL_END_TIME'] = form.glob_end.data

    # Iterate through keys
    for key in keys:
        new_value = new_settings[key]
        record = Settings.query.filter(Settings.settings_name == key).first()
        record = SettingsValues.query.filter(SettingsValues.settings_id_settings == record.id_settings).first()

        if record is not None:
            record.value = new_value

            try:
                db.session.commit()
            except (IntegrityError, InternalError) as e:
                db.session.rollback()
                current_app.logger.error('Database error occurred in: {}'.format(e.args[2]))
                result = False

    return result


def _get_glob_rules_settings():
    """Retrieves the global rule(s) settings from database

    :return dict glob_rules_settings:
    """

    glob_rules_settings = dict()

    _glob_rules = Settings.query \
        .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
        .filter(Settings.settings_name.like('GLOBAL%')) \
        .with_entities(Settings.settings_name, Settings.units, SettingsValues.value) \
        .all()

    for setting in _glob_rules:
        name = setting[0]
        value = ''

        if setting[1] == 'time':
            value= str(setting[2])
        elif setting[1] == 'integer':
            value = int(setting[2])

        glob_rules_settings[name] = value

    return glob_rules_settings


@bp.route('/settings/rules', methods=['GET', 'POST'])
@login_required
def rules_settings():
    """Route to rule settings

    :return html settings_rules.html:
    """
    form = GlobalTimeSettingsForm()
    save_result = False

    if request.method == 'POST':
        if form.validate():
            save_result = _save_glob_rules_settings(form)

    # Global Rule(s) Settings
    try:
        settings = _get_glob_rules_settings()
    except Exception as e:
        current_app.logger.error(e)
    else:
        weekdays = settings.get('GLOBAL_DAYS')

        form.glob_mon.data = True if ((weekdays & (1 << 0)) >> 0) else False
        form.glob_tue.data = True if ((weekdays & (1 << 1)) >> 1) else False
        form.glob_wed.data = True if ((weekdays & (1 << 2)) >> 2) else False
        form.glob_thr.data = True if ((weekdays & (1 << 3)) >> 3) else False
        form.glob_fri.data = True if ((weekdays & (1 << 4)) >> 4) else False
        form.glob_sat.data = True if ((weekdays & (1 << 5)) >> 5) else False
        form.glob_sun.data = True if ((weekdays & (1 << 6)) >> 6) else False
        form.glob_start.data = settings.get('GLOBAL_START_TIME', '00:00')
        form.glob_end.data = settings.get('GLOBAL_END_TIME', '00:00')

    return render_template('settings_rules/settings_rules.html', form=form, save_result=save_result)
