# coding: utf-8
"""
Dashboard
---------

Dashboard displays the current overview of system functions and recent events. It is a protected page and only those
with administrative access can view it.


"""
# Flask
from flask import render_template, Blueprint, jsonify, request, current_app
from flask_security import login_required

# Database tables and conversions
from marshmallow import Schema, fields
from sqlalchemy import and_, desc
from sqlalchemy.exc import OperationalError, InternalError, IntegrityError
from ..models import Events, User, ReaderSettings, ReaderStatus

# Cache
from ..extensions import cache

# System
from datetime import datetime, timedelta
import re
from subprocess import check_output, CalledProcessError


bp = Blueprint('site', __name__)


@cache.cached(timeout=50, key_prefix='get_health')
def _get_health():
    """Gets the current number of connected readers

    :returns int count: Number of readers 0 - 4
    """
    count = ReaderStatus.query.filter_by(status='CONNECTED').count()

    return 0 if count is None else count


@cache.cached(timeout=50, key_prefix='get_denied_count')
def _get_denied_count():
    """Gets the number of denied accesses in the last 24 hours

    :returns int denied_count: Count of denied
    """
    denied_count = User.query.join(Events, User.id == Events.user_id) \
        .with_entities(Events.event_type) \
        .filter(and_(Events.event_type == 'DENIED',
                     Events.event_time > (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S'),
                     Events.event_time < (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'))) \
        .count()

    return 0 if denied_count is None else denied_count


@cache.cached(timeout=50, key_prefix='get_valid_count')
def _get_valid_count():
    """Gets the number of approved accesses in the last 24 hours

    :returns int valid_count: Count of approved
    """
    valid_count = User.query.join(Events, User.id == Events.user_id) \
        .with_entities(Events.event_type) \
        .filter(and_(Events.event_type == 'ACCESS',
                     Events.event_time > (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S'),
                     Events.event_time < (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'))) \
        .count()

    return 0 if valid_count is None else valid_count


@cache.cached(timeout=50, key_prefix='get_error_count')
def _get_error_count():
    """Gets the current number of errors listed in the system logs

    :returns int errors: Number of errors on system
    """
    try:
        logs = check_output(['journalctl', '-t', 'modis-monitor', '-t', 'modis-admin', '--since',
                             (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')],
                            timeout=25).decode("utf-8")
    except CalledProcessError as e:
        current_app.logger.error(e)
        return 0
    else:
        return len(re.findall('error', logs.lower()))


@bp.route('/events', methods=['POST'])
@cache.cached(timeout=50, key_prefix='get_recent_events')
@login_required
def get_recent_events():
    """Pulls all events on the database

    Displays the user, location and type of event that occurred.

    This is rendered by `Datatables <http://www.datatables.net>`_ with a structure like:

    .. tabularcolumns:: |first_name|last_name|event_type|event_time|location_name|location_direction|

    :returns dict records: JSON object of records
    """

    if len(request.form) != 0:
        action = request.form.get('action')

        if action is not None:
            if action == 'request':
                try:
                    recent_events = User.query\
                        .join(Events, User.id == Events.user_id)\
                        .join(ReaderSettings, Events.reader_settings_id_reader == ReaderSettings.id_reader)\
                        .with_entities(User.first_name, User.last_name, Events.event_type, Events.event_time,
                                       ReaderSettings.location_name, ReaderSettings.location_direction) \
                        .filter(and_(Events.event_time < datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                     Events.event_time > (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')))\
                        .order_by(desc(Events.event_time)) \
                        .limit(100).all()
                except (OperationalError, InternalError, IntegrityError):
                    return jsonify({'data': ''})
                else:
                    class UserEvent(Schema):
                        first_name = fields.String()
                        last_name = fields.String()
                        event_type = fields.String()
                        event_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
                        location_name = fields.String()
                        location_direction = fields.String()

                    result, errors = UserEvent().dump(recent_events, many=True)

                    if errors:
                        current_app.logger.debug(errors)
                        return jsonify({'error': 'No records'})
                    else:
                        return jsonify({'data': result})

    return jsonify({'error': 'Poorly formed request'})


@bp.route('/')
@login_required
def index():
    """Index page.

    :returns html_template index.html:
    """
    health = False
    denied_count = 0
    valid_count = 0

    try:
        health = True if _get_health() > 0 else False
        denied_count = _get_denied_count()
        valid_count = _get_valid_count()
    except OperationalError:
        current_app.logger.error('Database Error')
    finally:
        data = {
            'errors': _get_error_count(),
            'health': health,
            'denied_count': denied_count,
            'valid_count': valid_count
        }

        return render_template('index/index.html', **data)
