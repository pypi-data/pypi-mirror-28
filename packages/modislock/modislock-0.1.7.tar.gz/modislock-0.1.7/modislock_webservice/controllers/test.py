# coding: utf-8
from flask import Blueprint, render_template, jsonify
from ..tasks import send_async_email, send_async_command, upgrade_modislock


bp = Blueprint('test', __name__)


@bp.route('/test')
def show_test():
    # from pyotp import TOTP, random_base32
    # import pyqrcode
    # from io import BytesIO
    # import base64
    #
    # qrcode = pyqrcode.create(TOTP(random_base32()).provisioning_uri('Richard Lowe', issuer_name='Modis Lock'))
    # buffer = BytesIO()
    # qrcode.png(buffer, scale=5)
    # b64 = str(base64.b64encode(buffer.getvalue()))[2:-1]
    #
    # data = {
    #     'user_name': 'Richard Lowe',
    #     'email_address': 'richard@modislab.com',
    #     'key': 'totp',
    #     'key_code': 7562,
    #     'key_image': b64
    # }
    # send_async_command.delay(['ls', '-la'])
    # send_async_email.delay('happy')
    upgrade_modislock.delay('Flask-HTMLmin')

    data = {
        'stuff': 'stuff to render'
    }

    return render_template('test/test.html', **data)

