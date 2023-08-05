# coding: utf-8
# Flask
from flask import (render_template, Blueprint, send_file, request, current_app, jsonify)
from flask_security import login_required

# Database
from ..models import (db, Events, SettingsValues, Settings)
from sqlalchemy.exc import InternalError, IntegrityError

# File handing
import gzip
import shutil

# OS
from datetime import datetime
import os
import sys
from subprocess import Popen, PIPE, TimeoutExpired
import re
from io import BytesIO

# Async
from ..tasks import send_async_command


bp = Blueprint('settings_backup', __name__)

ALLOWED_EXTENSIONS = {'mod', 'zip'}


def allowed_file(filename):
    """Allowed file extension types that will be accepted on restore

    :param str filename:
    :return str filename:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/settings/backup/run_backup', methods=['POST'])
@login_required
def backup_db():
    """Backs up database from dump, compresses and uploads to client

    :return file db_backup: Returns a compressed database file with timestamp and suffix of .mod
    """
    db_config = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    p = re.compile(r'[/]{2}([\w]+):([\w]+)@([a-zA-Z0-9._\-]+)/([\w]+)')
    m = p.search(db_config)
    # args = ['mysqldump', '-u', m.group(1), '-p' + m.group(2), '-h', m.group(3), '--databases', m.group(4)]
    args = ['mysqldump', '-u', 'root', '-h', m.group(3), '--databases', m.group(4)]

    p1 = Popen(args, stdout=PIPE)
    p2 = Popen('gzip', stdin=p1.stdout, stdout=PIPE)
    cmd_data = p2.communicate(timeout=60)[0]

    current_app.logger.debug('Database is backed up in the pipe, now sending to stream')

    last_bu = SettingsValues.query.join(Settings, SettingsValues.settings_id_settings == Settings.id_settings) \
        .filter(Settings.settings_name == 'LAST_BACKUP') \
        .first()

    bu_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if last_bu is not None:
        last_bu.value = bu_datetime
        db.session.commit()

    return send_file(BytesIO(cmd_data), attachment_filename='lock' + bu_datetime + '.mod', as_attachment=True)


@bp.route('/settings/backup/run_restore', methods=['GET', 'POST'])
@login_required
def restore_db():
    """Restores database from downloaded file

    :return bool result: True / False based on operation results
    """
    if request.method == 'POST':
        assert 'file' in request.files
        upload_file = request.files['file']

        if allowed_file(upload_file.filename):
            upload_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], upload_file.filename))
            upload_file = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_file.filename)
            restore_file = os.path.join(current_app.config['UPLOAD_FOLDER'], 'restore.sql')
            status = True

            try:
                with gzip.open(upload_file, 'rb') as f:
                    with open(restore_file, 'wb') as f_out:
                        shutil.copyfileobj(f, f_out)
            except:
                os.remove(upload_file)
                status = False
            else:
                db_config = current_app.config.get('SQLALCHEMY_DATABASE_URI')
                p = re.compile(r'[/]{2}([\w]+):([\w]+)@([a-zA-Z0-9._\-]+)/([\w]+)')
                m = p.search(db_config)
                # args = ['mysql', m.group(4), '-u', m.group(1), '-p' + m.group(2), '-h', m.group(3)]
                args = ['mysqldump', '-u', 'root', '-h', m.group(3), '--databases', m.group(4)]

                proc = Popen(args, stdin=PIPE, stdout=PIPE)
                restore_file = 'SOURCE ' + restore_file + ';\nexit\n'

                db.session.remove()  # Remove the session so the database tables are not locked

                try:
                    outs, errs = proc.communicate(restore_file.encode(), timeout=30)
                except TimeoutExpired:
                    proc.kill()
                    outs, errs = proc.communicate()
                    status = False
                    current_app.logger.error('ERROR: Restoring database failed on communication with database')
                finally:
                    os.remove(upload_file)
                    os.remove('restore.sql')
            finally:
                result = 'success' if status else 'error'
                msg = 'database restored' if status else 'database restoration failed'
                code = 201 if status else 500
                return jsonify({result: msg}), code
    else:
        current_app.logger.error('ERROR: File provided for database restore is not valid')
        return False


@bp.route('/settings/reboot')
@login_required
def reboot():
    return render_template('settings_backup/system_rebooting.html',
                           domain=current_app.config.get('SITE_DOMAIN'))


@bp.route('/settings/backup', methods=['GET', 'POST'])
@login_required
def backup_settings():
    """Backup endpoint

    :return html settings_backup.html:
    """
    if request.method == 'POST':
        if request.form['action'] == 'reboot':
            args = ['systemctl', 'reboot']

            try:
                current_app.logger.info('Sending reboot command')
                send_async_command.apply_async(args=[args], countdown=3)
            except:
                current_app.logger.error('Send of reboot command failed: {}'.format(sys.exc_info()[0]))
                return jsonify({'error': 'unabled to send reboot command'}), 500
            else:
                return jsonify({'success': 'rebooting'}), 201

        elif request.form['action'] == 'purge':
            Events.query.delete()

            try:
                db.session.commit()
            except (InternalError, IntegrityError):
                current_app.logger.error('ERROR: Purging events from database failed')
            else:
                current_app.logger.info('Purged all events from database')
            finally:
                return jsonify({'success': 'purged database'}), 201
    else:
        last_bu = SettingsValues.query \
            .join(Settings, SettingsValues.settings_id_settings == Settings.id_settings) \
            .filter(Settings.settings_name == 'LAST_BACKUP') \
            .first()
        if last_bu is not None:
            back_age = (datetime.now() - datetime.strptime(last_bu.value, '%Y-%m-%d %H:%M:%S')).days
        else:
            back_age = 0

        return render_template('settings_backup/settings_backup.html', backup_age=back_age)
