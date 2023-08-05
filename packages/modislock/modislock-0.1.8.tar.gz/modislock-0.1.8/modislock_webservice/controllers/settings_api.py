# coding: utf-8

# Flask
from flask import render_template, Blueprint, request, abort, current_app, jsonify
from flask_security import login_required

# Database
from ..models import AppApi, AppApiAccess, ma, db
from marshmallow import fields
from sqlalchemy.exc import IntegrityError, InternalError, DataError

# Password
from werkzeug.security import generate_password_hash
import uuid

# OS
from collections import defaultdict
import re

# Misc
from datetime import datetime, timedelta


bp = Blueprint('settings_api', __name__)


def _get_request_data(form):
    """Returns a dictionary from multidictionary objects

    return dict list with data from request.form
    request.form comes in multidict [('data[id][field]',value), ...]
    :param form: MultiDict from `request.form`
    :rtype: {id1: {field1:val1, ...}, ...} [fieldn and valn are strings]
    """
    # fill in id field automatically
    data = defaultdict(lambda: {})

    # fill in data[id][field] = value
    for form_key in form.keys():
        if form_key == 'action':
            continue
        data_part, id_part, field_part = form_key.split('[')

        if data_part != 'data':
            raise ValueError("invalid input in request: {}".format(form_key))

        id_value = int(id_part[0:-1])
        field_name = field_part[0:-1]
        data[id_value][field_name] = form[form_key]
    return data  # return decoded result


def _generate_pass_token(secret_pwd):
    hashed_password = generate_password_hash(secret_pwd)
    expires = datetime.utcnow().replace(second=0, microsecond=0) + timedelta(days=30)
    token = str(uuid.uuid4())

    return hashed_password, expires, token


@bp.route('/settings/api')
@login_required
def api_settings():
    return render_template('settings_api/settings_api.html')


@bp.route('/settings/api/api_tokens', methods=['GET', 'PUT', 'POST', 'DELETE'])
@login_required
def get_api_tokens():
    re_field = re.compile(r'^data\[\w+\]\[(\w+)\]$')

    if request.method == 'GET':
        api_keys = AppApi.query.join(AppApiAccess, AppApi.app_api_id == AppApiAccess.app_api_app_api_id) \
            .with_entities(AppApi.app_api_id.label('app_id'),
                           AppApiAccess.token,
                           AppApiAccess.expires) \
            .all()

        if api_keys is None:
            return jsonify({'data': []}), 200
        else:
            class ApiKey(ma.Schema):
                app_id = fields.String()
                token = fields.String()
                expires = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

            ret = ApiKey(many=True).dump(api_keys).data

            return jsonify({'data': ret}), 200
    elif request.method == 'POST':
        action = request.form.get('action')

        if action != 'create' or action is None:
            abort(400)

        try:
            action = _get_request_data(request.form.to_dict())
        except ValueError:
            return jsonify({'error': 'ERROR_IN_REQUEST'})

        app_id = action[0].get('app_id')
        app_secret = action[0].get('app_secret')

        existing_app = AppApi.query.filter_by(app_api_id=app_id).first()

        if existing_app:
            error = {
                'code': 'APP_ID_ALREADY_EXISTS'
            }
            return jsonify({'error': error}), 400
        else:
            pwd, exp, tok = _generate_pass_token(app_secret)

            app = AppApi(app_api_id=app_id,
                         app_secret=pwd)
            access = AppApiAccess(token=tok,
                                  expires=exp,
                                  app_api_app_api_id=app.app_api_id)
            db.session.add(app)
            db.session.add(access)

            try:
                db.session.commit()
            except (IntegrityError, InternalError, DataError) as e:
                db.session.rollback()
                current_app.logger.debug('Error in database operation {}'.format(e.args[0]))
                return jsonify({'error': 'ERROR_ADDING_TO_DATABASE'})
            else:
                return jsonify({'data': [
                    {'app_id': app_id,
                     'token': tok,
                     'expires': exp
                     }
                ]}), 201
    elif request.method == 'PUT':
        action = request.form.get('action')

        if action != 'edit' or action is None:
            abort(400)

        action = request.form.to_dict()
        form_request = dict()

        for key in action.keys():
            if key == 'action':
                continue
            result = re_field.match(key)
            form_request[result.group(1)] = action[key]

        edit_app = AppApi.query.join(AppApiAccess, AppApi.app_api_id == AppApiAccess.app_api_app_api_id)\
            .filter(AppApi.app_api_id == form_request.get('app_id')).one_or_none()

        if edit_app is not None:
            pwd, exp, tok = _generate_pass_token(form_request.get('app_secret'))
            edit_app.app_secret = pwd
            edit_app.token = tok
            edit_app.expires = exp
            try:
                db.session.commit()
            except (IntegrityError, InternalError, DataError) as e:
                db.session.rollback()
                current_app.logger.debug('Error in database operation {}'.format(e.args[0]))
                return jsonify({'error': 'COULD_NOT_COMMIT_CHANGES'})

            return jsonify({'data': [{
                'app_id': edit_app.app_api_id,
                'token': edit_app.token,
                'expires': edit_app.expires
            }]}), 200
    elif request.method == 'DELETE':
        action = request.args.get('action')

        if action != 'remove' or action is None:
            abort(400)

        action = request.args.to_dict()
        arg_request = dict()

        for key in action.keys():
            if key == 'action':
                continue
            result = re_field.match(key)
            arg_request[result.group(1)] = action[key]

        del_app = AppApi.query.filter_by(app_api_id=arg_request.get('app_id')).one_or_none()

        if del_app is not None:
            db.session.delete(del_app)

            try:
                db.session.commit()
            except (InternalError, IntegrityError) as e:
                current_app.logger.error('Count not delete record from database: {}'.format(e.args[0]))
                return jsonify({'error': 'COULD_NOT_DELETE_RECORD'})
            else:
                return jsonify({}), 204
        else:
            abort(400)


