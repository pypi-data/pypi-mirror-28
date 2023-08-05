# coding: utf-8

# Flask and DB
from flask_restful import Resource, reqparse

# Validators
from .decorators import app_required

# Utilites
from modislock_webservice.utils.key_generators import gen_unique_pin, gen_unique_webcode

# Database
from modislock_webservice.models import ReaderStatus, Sensors, Readings, db

# System
from subprocess import Popen, PIPE
import re


parser = reqparse.RequestParser()
parser.add_argument('feature',
                    required=True,
                    choices=('key_gen', 'totp_gen', 'sys_temp', 'reader_status', 'door_sensors'),
                    help='Invalid feature, [key_gen, totp_gen, sys_temp, reader_status, door_sensors] are the only '
                         'valid choices',
                    location='args')


def _get_temps():
    """Gets the current case and cpu temps

    :return dict temps: Case and CPU temps
    """
    case_temp = None
    cpu_temp = None
    cpu = None
    case = None

    try:
        case_temp = Popen(['sensors', 'ds3231-i2c-1-68'], stdout=PIPE)
        case, errs = case_temp.communicate(timeout=5)
    except (TimeoutError, FileNotFoundError):
        if case_temp is not None:
            case_temp.kill()

    try:
        cpu_temp = Popen(['/DietPi/dietpi/dietpi-cpuinfo'], stdout=PIPE)
        cpu, errs = cpu_temp.communicate(timeout=5)
    except (TimeoutError, FileNotFoundError):
        if cpu_temp is not None:
            cpu_temp.kill()

    case_measurement = '38.1'
    cpu_measurement = '41'

    if case is not None:
        for lines in case:
            if 'temp' in lines:
                m = re.search(r' [+-]?(\d{1,3}.\d?)', lines)
                if m is not None:
                    case_measurement = m.group(1)

    if cpu is not None:
        for lines in cpu:
            if 'Temp' in lines:
                m = re.search(r' ?(\d+)\'c', lines)
                if m is not None:
                    cpu_measurement = m.group(1)

    return cpu_measurement, case_measurement


def _get_reader_status():
    slaves = ReaderStatus.query.with_entities(ReaderStatus.reader_id_reader, ReaderStatus.status) \
        .all()

    readers = dict()

    if slaves is not None:
        for reader in slaves:
            readers[reader.reader_id_reader] = reader.status

    return readers


def _get_door_status():
    sensors = Sensors.query.with_entities(Sensors.id_sensors, Sensors.name, Readings.value) \
        .join(Readings, Readings.sensors_id_sensors == Sensors.id_sensors) \
        .filter(Sensors.name.like("DOOR%")) \
        .all()

    doors = dict()

    if sensors is not None:
        for sensor in sensors:
            doors['1' if sensor.name == 'DOOR 1' else '2'] = sensor.value

    return doors


class UtilsAPI(Resource):
    """Various utilities exposed through API calls

    """

    decorators = [app_required]

    def get(self):
        """Various system utilities

        .. http:get:: /api/v1.0/utils?feature=(string:requested_feature)

        Valid features are:
            `key_gen` A unique PIN code used in multiple protocols. This PIN is guaranteed to be unique.
            `totp_gen` A unique challenge generated for TOTP enrollments
            `sys_temp` Current system temperature
            `reader_status` Not yet implemented
            `door_sensors` Not yet implemented

        **Example TOTP**

        .. sourcecode:: http

            GET /api/v1.0/utils?feature=totp_gen HTTP/1.1
            Host: modislock.local
            Accept: application/json, text/javascript

        **Example Response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
                "message": {
                    "totp_code": "7YVYAQQ3UQMJXXOJ"
                }
            }

        **Example Reader Status**

        .. sourcecode:: http

            GET /api/v1.0/utils?feature=reader_status HTTP/1.1
            Host: modislock.local
            Accept: application/json, text/javascript

        **Example Response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
                "message": {
                    "1": "DISCONNECTED",
                    "2": "DISCONNECTED",
                    "3": "DISCONNECTED",
                    "4": "DISCONNECTED"
                }
            }

        **Example Door Status**

        .. sourcecode:: http

            GET /api/v1.0/utils?feature=door_status HTTP/1.1
            Host: modislock.local
            Accept: application/json, text/javascript

        **Example Response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
                 "message": {
                     "1": "INACTIVE",
                     "2": "INACTIVE"
                 }
            }

        :reqheader Authorization: X-APP-ID / X-APP-PASSWORD or X-APP-TOKEN (Password or Token generated by administration)

        :statuscode 200: No errors have occurred
        :statuscode 403: Credentials missing for api usage
        """
        args = parser.parse_args(strict=True)
        message = dict()

        if args.feature == 'key_gen':
            message['pin_code'] = gen_unique_pin()
        elif args.feature == 'totp_gen':
            message['totp_code'] = gen_unique_webcode()
        elif args.feature == 'sys_temp':
            cpu, case = _get_temps()
            message['cpu'] = cpu
            message['case'] = case
        elif args.feature == 'reader_status':
            message = _get_reader_status()
        elif args.feature == 'door_sensors':
            message = _get_door_status()

        return {'message': message}
