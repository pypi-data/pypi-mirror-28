# coding: utf-8

# Flask
from flask import (render_template, Blueprint, request, jsonify, current_app)
from flask_security import login_required
from ..utils.system_info import SystemInfo

# Cache
from ..extensions import cache

# System libraries
from subprocess import check_output, CalledProcessError

# Time and Timezone information
from datetime import datetime, timedelta
from tzlocal import get_localzone

# Database
from ..models import ReaderStatus, Readings, Sensors, Settings, SettingsValues

# Timezone form
from ..forms import TimeZoneSettings

# Upgrade
from pip.utils import get_installed_version
from xmlrpc.client import ServerProxy
from celery.result import AsyncResult
from modislock_webservice.tasks import send_async_command, upgrade_modislock


bp = Blueprint('system', __name__)


@cache.cached(timeout=60, key_prefix='get_log_info')
def get_log_info():
    """Retrieves system journal

    :returns str logs: Log entries for lock
    """
    try:
        logs = check_output(['journalctl', '-t', 'modis-monitor', '-t', 'modis-admin', '--since',
                             (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')],
                            timeout=25).decode("utf-8")
    except CalledProcessError as e:
        current_app.logger.error(e)
        return 'No Logs'
    else:
        return logs


@bp.route('/system/status', methods=['GET'])
def get_status():
    """Retrieves various system information

    .. sourcecode:: sql

       SELECT id_sensors, name, readings.value
       FROM readings JOIN sensors ON readings.sensors_id_sensors = sensors.id_sensors
       WHERE sensors.name LIKE 'DOOR%';

    :returns: System Data

    :rtype: {'uptime': (str), 'memory_total': (int), 'memory_free': (int), 'memory_usage': (int), 'storage':(float), 'time': (datetime), 'cpu_load': (float), 'sensors': (dict), 'readers': (dict)}
    """
    sysinfo = SystemInfo.get_system_info()

    readers = ReaderStatus.query.with_entities(ReaderStatus.reader_id_reader, ReaderStatus.status)\
        .all()

    sensors = Sensors.query.with_entities(Sensors.id_sensors, Sensors.name, Readings.value)\
        .join(Readings, Readings.sensors_id_sensors == Sensors.id_sensors)\
        .filter(Sensors.name.like("DOOR%"))\
        .all()

    doors = dict()
    remotes = dict()

    for sensor in sensors:
        doors['1' if sensor.name == 'DOOR 1' else '2'] = sensor.value

    for reader in readers:
        remotes[reader.reader_id_reader] = reader.status

    disks = SystemInfo.get_disks()

    data = {
        'uptime': str(timedelta(seconds=sysinfo.get('uptime'))).split('.')[0],
        'memory_total': SystemInfo.get_memory()[0],
        'memory_free': SystemInfo.get_memory()[1],
        'memory_usage': SystemInfo.get_memory()[2],
        'storage': disks[0].get('space_used_percent'),
        'time': datetime.now(tz=None).strftime("%H:%M:%S"),
        'cpu_load': sysinfo.get('load_avg'),
        'sensors': doors,
        'readers': remotes
    }

    return jsonify(data)


@bp.route('/system/upgrade/<string:target>')
def system_upgrade(target):
    """Upgrades selected system

    :param str target:

    :return html system_upgrading.html:
    """
    if target == 'modislock':
        task_id = upgrade_modislock.s('modislock').apply_async()
    elif target == 'modislock-monitor':
        task_id = upgrade_modislock.s('modislock-monitor').apply_async()
    else:
        task_id = 0

    domain = current_app.config.get('SITE_DOMAIN')

    return render_template('system/system_upgrading.html', target=target, task_id=task_id.id, domain=domain)


@bp.route('/system/upgrade_status/<string:task_id>')
def task_status(task_id):
    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'message': task.info.get('message', ''),
            'count': task.info.get('count', '')
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'message': task.info.get('message', ''),
            'count': task.info.get('count', '')
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'message': task.info.get('message', ''),
            'count': task.info.get('count', '')
        }
    else:
        response = {
            'state': task.state,
            'message': task.info.get('message', ''),
            'count': task.info.get('count', '')
        }

    return jsonify(response)


@bp.route('/system/restart', methods=['POST'])
def task_complete():
    if request.method == 'POST':
        target = request.form.get('target')
        args = ['supervisorctl', 'restart']

        if target == 'modislock':
            args.append('admin:*')
        elif target == 'modislock-monitor':
            args.append('monitor:*')
        elif target == 'modislock-system':
            args = ['systemctl', 'reboot']
            send_async_command.apply_async(args=[args], countdown=3)

        if len(args) > 2:
            send_async_command.apply_async(args=[args])

    return jsonify({'success': 0}), 200


@bp.route('/system', methods=['GET', 'POST'])
@login_required
def system():
    """System Information Page

    :return html system.html:
    """
    form = TimeZoneSettings()
    pypi = ServerProxy('https://pypi.python.org/pypi')

    # Setting time
    if request.method == 'POST':
        if form.validate():
            new_zone = form.tz_zone.data

            zargs = ['timedatectl', 'set-timezone', new_zone]
            ztask = send_async_command.apply_async(args=[zargs])
            zresult = ztask.get()
            current_app.logger.debug('Result of zone setting: {}'.format(zresult))
            # TODO return result

            targs = ['timedatectl', 'set-time', str(form.hours.data) + ':' + str(form.minutes.data) + ':00']
            ttask = send_async_command.apply_async(args=[targs])
            tresult = ttask.get()
            current_app.logger.debug('Result of time setting: {}'.format(tresult))
            # TODO return result

    form.tz_zone.data = get_localzone().zone

    serial = Settings.query \
        .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
        .filter(Settings.settings_name == 'SERIAL_NUMBER') \
        .with_entities(Settings.settings_name, SettingsValues.value) \
        .one_or_none()

    app_version = get_installed_version('modislock')
    app_version = app_version if app_version is not None else '0.1.0'
    mon_version = get_installed_version('modislock-monitor')
    mon_version = mon_version if mon_version is not None else '0.1.0'

    try:
        app_avail_version = pypi.package_releases('modislock')[0]
    except (KeyError, IndexError):
        app_avail_version = '0.1.0'
    try:
        mon_avail_version = pypi.package_releases('modislock-monitor')[0]
    except (KeyError, IndexError):
        mon_avail_version = '0.1.0'

    serial_number = 'Unknown'

    if serial is not None:
        serial_number = serial.value

    data = {
        'app_version': app_version,
        'app_avail_version': app_avail_version,
        'mon_version': mon_version,
        'mon_avail_version': mon_avail_version,
        'serial_number': serial_number,
        'time_zone': get_localzone().zone,
        'time_zone_settings': form,
        'logs': get_log_info()
    }

    return render_template('system/system.html', **data)
