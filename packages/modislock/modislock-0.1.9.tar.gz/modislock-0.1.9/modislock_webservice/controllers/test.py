# coding: utf-8
from flask import Blueprint, render_template, jsonify
from ..tasks import send_async_email, send_async_command, upgrade_modislock


bp = Blueprint('test', __name__)


@bp.route('/test')
def show_test():
    upgrade_modislock.delay('tzlocal')

    data = {
        'stuff': 'stuff to render'
    }

    return render_template('test/test.html', **data)

