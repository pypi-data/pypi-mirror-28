# coding: utf-8

# Flask
from flask import (render_template, Blueprint, request, jsonify, current_app, redirect, url_for)
from flask_security import login_required
from ..utils.system_info import SystemInfo
from ..utils.sys_rtc import ntp_clock_sync, time_zone

# Cache
from ..extensions import cache

# System libraries
from subprocess import check_output, CalledProcessError

# Time and Timezone information
from datetime import datetime, timedelta

# Database
from ..models import ReaderStatus, Readings, Sensors, Settings, SettingsValues

# Timezone form
from ..forms import TimeZoneSettings

# Upgrade
from pip.utils import get_installed_version
from socket import gaierror
from xmlrpc.client import ServerProxy
from celery.result import AsyncResult
from ..tasks import send_async_command, upgrade_modislock


bp = Blueprint('system', __name__)


def _get_serial_number():
    """Gets the system serial number

    :return:
    """
    serial_number = '0'

    serial = Settings.query \
        .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
        .filter(Settings.settings_name == 'SERIAL_NUMBER') \
        .with_entities(Settings.settings_name, SettingsValues.value) \
        .one_or_none()

    if serial is not None:
        serial_number = serial.value

    return serial_number


@cache.cached(timeout=120, key_prefix='get_software_versions')
def _get_software_versions():
    """Get the installed versions and available versions

    :return:
    """
    pypi = ServerProxy('https://pypi.python.org/pypi')

    app_version = get_installed_version('modislock')
    app_version = app_version if app_version is not None else '0.1.0'
    mon_version = get_installed_version('modislock-monitor')
    mon_version = mon_version if mon_version is not None else '0.1.0'

    try:
        app_avail_version = pypi.package_releases('modislock')[0]
    except (KeyError, IndexError, gaierror):
        app_avail_version = '0.1.0'

    try:
        mon_avail_version = pypi.package_releases('modislock-monitor')[0]
    except (KeyError, IndexError, gaierror):
        mon_avail_version = '0.1.0'

    return {'app': app_version, 'app_avail': app_avail_version, 'mon': mon_version, 'mon_avail': mon_avail_version}


def _save_time_info(form):
    """Saves timezone and timedate information

    :param form:
    :return:
    """
    if time_zone() != form.tz_zone.data:
        zargs = ['timedatectl', 'set-timezone', form.tz_zone.data]

        try:
            ztask = send_async_command.apply_async(args=[zargs])
        except:
            current_app.logger.error('Error sending task to worker')
        else:
            zresult = ztask.get()
            current_app.logger.debug('Result of zone setting: {}'.format(zresult))

    if form.auto_time.data != ntp_clock_sync():
        ntp_clock_sync(enabled=form.auto_time.data)

    if not form.auto_time.data:
        try:
            targs = ['timedatectl', 'set-time', form.sys_time.data]
            ttask = send_async_command.apply_async(args=[targs])
        except:
            current_app.logger.error('Error sending task to worker')
        else:
            tresult = ttask.get()
            current_app.logger.debug('Result of time setting: {}'.format(tresult))


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
    task_id = 0

    if target == 'modislock':
        try:
            task_id = upgrade_modislock.s('modislock').apply_async(countdown=3)
        except:
            current_app.logger.debug('Could not upgrade modislock')
    elif target == 'modislock-monitor':
        try:
            task_id = upgrade_modislock.s('modislock-monitor').apply_async(countdown=3)
        except:
            current_app.logger.debug('Could not upgrade monitor')
    else:
        task_id = 0

    if task_id == 0:
        return redirect(url_for('system.system')), 302
    else:
        domain = current_app.config.get('SITE_DOMAIN')
        return render_template('system/system_upgrading.html', target=target, task_id=task_id.id, domain=domain)


@bp.route('/system/upgrade_status/<string:task_id>')
def task_status(task_id):
    """Gets the requested task update status

    :param task_id:
    :return:
    """
    task = AsyncResult(task_id)

    response = {'state': 'PENDING', 'message': 'Pending Execution', 'count': 0}

    if task.state == 'FAILURE':
        response['state'] = task.state
        response['message'] = task.info.get('message', '')
        response['count'] = 0
    elif task.state == 'COMPLETE':
        response['state'] = task.state
        response['message'] = task.info.get('message', '')
        response['count'] = task.info.get('count', '')
    elif task.state == 'PROGRESS':
        response['state'] = task.state
        response['message'] = task.info.get('message', '')
        response['count'] = task.info.get('count', '')

    return jsonify(response)


@bp.route('/system/restart', methods=['POST'])
def task_complete():
    """When a task is complete, restart the required systems

    :return:
    """

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

    # Setting time
    if request.method == 'POST':
        if form.validate():
            _save_time_info(form)

    form.tz_zone.data = time_zone()
    form.auto_time.data = ntp_clock_sync()

    software = _get_software_versions()

    data = {
        'app_version': software['app'],
        'app_avail_version': software['app_avail'],
        'mon_version': software['mon'],
        'mon_avail_version': software['mon_avail'],
        'serial_number': _get_serial_number(),
        'time_zone': time_zone(),
        'time_zone_settings': form,
        'logs': get_log_info()
    }

    return render_template('system/system.html', **data)
