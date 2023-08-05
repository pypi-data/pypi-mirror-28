# coding: utf-8

# Flask
from flask import (render_template, Blueprint, request, current_app)
from flask_security import login_required
from ..forms import ReaderSettingsForm, OutputSettingsForm

# Database
from ..models import db, Settings, ReaderSettings, SettingsValues
from sqlalchemy.exc import InternalError, IntegrityError


bp = Blueprint('settings_reader', __name__)


def _save_reader_settings(form):
    """Saves all changed reader settings to database

    :param form form:
    """
    old_settings = _get_reader_settings()
    keys = set(old_settings.keys())
    result = True

    # Submits
    new_settings = dict()
    # Reader 1
    reader1 = form.reader1.data
    reader1_dir = form.reader1_dir.data
    reader1_relay = form.reader1_relay.data
    new_settings[1] = [reader1, reader1_dir, reader1_relay]
    # Reader 2
    reader2 = form.reader2.data
    reader2_dir = form.reader2_dir.data
    reader2_relay = form.reader2_relay.data
    new_settings[2] = [reader2, reader2_dir, reader2_relay]
    # Reader 3
    reader3 = form.reader3.data
    reader3_dir = form.reader3_dir.data
    reader3_relay = form.reader3_relay.data
    new_settings[3] = [reader3, reader3_dir, reader3_relay]
    # Reader 4
    reader4 = form.reader4.data
    reader4_dir = form.reader4_dir.data
    reader4_relay = form.reader4_relay.data
    new_settings[4] = [reader4, reader4_dir, reader4_relay]

    relays = Settings.query.with_entities(Settings.id_settings, Settings.settings_name) \
        .filter(Settings.settings_name.like('RELAY_' + '%' + '_ENABLED')).all()
    relay1_id = 0
    relay2_id = 0

    for relay in relays:
        if '1' in relay[1]:
            relay1_id = relay[0]
        elif '2' in relay[1]:
            relay2_id = relay[0]

    for key in keys:
        if old_settings[key] != new_settings[key]:
            #  Read the database entry
            reader = ReaderSettings.query.filter_by(id_reader=key).first()

            reader.location_name = new_settings[key][0]
            reader.location_direction = 'ENTRY' if new_settings[key][1] is True else 'EXIT'
            reader.settings_id_settings = relay1_id if new_settings[key][2] is True else relay2_id

            try:
                db.session.commit()
            except (IntegrityError, InternalError) as e:
                result = False
                current_app.logger.error('Error reading database: {}'.format(e.args[2]))

    return result


def _get_reader_settings():
    """Retrieve reader settings

    ..note: SELECT id_reader, location_name, location_direction, settings_name
    FROM reader_settings
    JOIN settings ON reader_settings.settings_id_settings = settings.id_settings
    JOIN settings_values ON settings.id_settings = settings_values.settings_id_settings
    """
    readers = dict()

    _readers = ReaderSettings.query.join(Settings).join(SettingsValues) \
        .with_entities(ReaderSettings.id_reader,
                       ReaderSettings.location_name,
                       ReaderSettings.location_direction,
                       Settings.settings_name) \
        .filter(ReaderSettings.id_reader > 0) \
        .all()

    for reader in _readers:
        readers[reader[0]] = [reader[1],
                              True if reader[2] is 'ENTRY' else False,
                              True if 'RELAY_1' in reader[3] else False]

    return readers


def _save_outputs_settings(form):
    """Saves the various outputs and their settings

    :param form form:

    """
    old_settings = _get_outputs_settings()
    keys = set(old_settings.keys())
    new_settings = dict()
    result = True

    new_settings[form.output_1.short_name.upper()] = form.output_1.data
    new_settings[form.output_2.short_name.upper()] = form.output_2.data
    new_settings[form.relay_1_delay.short_name.upper()] = form.relay_1_delay.data
    new_settings[form.relay_1_enabled.short_name.upper()] = form.relay_1_enabled.data
    new_settings[form.relay_2_delay.short_name.upper()] = form.relay_2_delay.data
    new_settings[form.relay_2_enabled.short_name.upper()] = form.relay_2_enabled.data

    for key in keys:
        try:
            if old_settings[key] != new_settings[key]:
                record = Settings.query.filter(Settings.settings_name == key).first()

                if record is not None:
                    if record.units == 'boolean':
                        value = 'ENABLED' if new_settings[key] is True else 'DISABLED'
                    else:
                        value = new_settings[key]

                    record = SettingsValues.query.filter(SettingsValues.settings_id_settings == record.id_settings) \
                        .first()
                    record.value = value

                    try:
                        db.session.commit()
                    except (IntegrityError, InternalError) as e:
                        db.session.rollback()
                        current_app.logger.error('Database error occurred in: {}'.format(e.args[2]))
                        result = False
                        continue
                else:
                    continue

        except KeyError:
            continue

    return result


def _get_outputs_settings():
    """Retrieves output settings from database and formats them for use in form

    :return dict outputs: Output settings
    """
    outputs = dict()

    _outputs = Settings.query.join(SettingsValues) \
        .with_entities(Settings.settings_name, Settings.units, SettingsValues.value) \
        .filter(Settings.settings_group_name == 'MONITOR') \
        .all()

    for output in _outputs:
        name = output[0]
        value = 0

        if output[1] == 'boolean':
            value = True if output[2] == 'ENABLED' else False
        elif output[1] == 'integer':
            value = int(output[2])
        elif output[1] == 'float':
            value = float(output[2])

        outputs[name] = value

    return outputs


@bp.route('/settings/reader', methods=['GET', 'POST'])
@login_required
def reader_settings():
    """Reader settings endpoint

    :return html settings_reader.html:
    """

    readers = ReaderSettingsForm()
    outputs = OutputSettingsForm()
    save_result = False

    if request.method == 'POST':
        form = request.form.get('submit_btn', None)

        if form is not None:
            if 'Reader' in form:
                if readers.validate():
                    save_result = _save_reader_settings(readers)
            elif 'Outputs' in form:
                if outputs.validate():
                    save_result = _save_outputs_settings(outputs)
    try:
        settings = _get_reader_settings()
    except ValueError as e:
        current_app.logger.error(e)
    else:
        # ID, NAME, DIRECTION, RELAY
        readers.reader1.data = settings[1][0]
        readers.reader1_dir.data = settings[1][1]
        readers.reader1_relay.data = settings[1][2]
        readers.reader2.data = settings[2][0]
        readers.reader2_dir.data = settings[2][1]
        readers.reader2_relay.data = settings[2][2]
        readers.reader3.data = settings[3][0]
        readers.reader3_dir.data = settings[3][1]
        readers.reader3_relay.data = settings[3][2]
        readers.reader4.data = settings[4][0]
        readers.reader4_dir.data = settings[4][1]
        readers.reader4_relay.data = settings[4][2]

    # Outputs settings
    try:
        settings = _get_outputs_settings()
    except ValueError as e:
        current_app.logger.error(e)
    else:
        outputs.relay_1_enabled.data = settings.get('RELAY_1_ENABLED', 'True')
        outputs.relay_2_enabled.data = settings.get('RELAY_2_ENABLED', 'True')
        outputs.output_1.data = settings.get('OUTPUT_1', '')
        outputs.output_2.data = settings.get('OUTPUT_2', '')
        outputs.relay_1_delay.data = settings.get('RELAY_1_DELAY', '')
        outputs.relay_2_delay.data = settings.get('RELAY_2_DELAY', '')

    return render_template('settings_reader/settings_reader.html', readers=readers, outputs=outputs,
                           save_result=save_result)
