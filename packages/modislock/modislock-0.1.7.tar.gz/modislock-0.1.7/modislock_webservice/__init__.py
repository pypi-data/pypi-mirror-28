# coding: utf-8

"""Modis Lock Administration

"""

# System libs
import logging
import sys
import os
from time import sleep

# Flask
from flask import Flask, render_template, Blueprint, redirect, url_for
from flask_security import SQLAlchemyUserDatastore

# CSRF Error
from flask_wtf.csrf import CSRFError
from jinja2 import ChoiceLoader, FileSystemLoader

# Journal logging
from systemd import journal
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.wsgi import SharedDataMiddleware

# Configuration
from .config import load_config

# API Resources
from .controllers.api import UserAPI, UsersAPI, KeyAPI, UtilsAPI, EventAPI
from .extensions import (
    security,
    marshmallow,
    csrf_protect,
    html_min,
    cache,
    mail,
    celery,
    assets,
    debug_toolbar,
    rest_api,
    asset_bundles
)

# Database
from .models import db, Settings, SettingsValues, User
from sqlalchemy import text

# Tasks
from .tasks import send_security_email

# Mail

# Insert project root path to sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))

if project_path not in sys.path:
    sys.path.insert(0, project_path)


def _import_submodules_from_package(package):
    import pkgutil

    modules = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix=package.__name__ + "."):
        modules.append(__import__(modname, fromlist="dummy"))
    return modules


def _load_mail_settings(app):
    """Load email settings on initialization from the database and apply them to the application

    :param app app:
    """
    with app.app_context():
        _mail_settings = Settings.query \
            .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
            .filter(Settings.settings_name.like('MAIL%')) \
            .with_entities(Settings.settings_name, SettingsValues.value) \
            .all()

        mail_settings = dict()

        for record in _mail_settings:
            try:
                mail_settings[record[0]] = record[1]
            except KeyError:
                continue

        # Mail support
        if len(mail_settings) > 0:
            app.config['MAIL_SERVER'] = mail_settings.get('MAIL_SERVER', '')
            app.config['MAIL_PORT'] = mail_settings.get('MAIL_PORT', 0)
            app.config['MAIL_USE_TLS'] = True if mail_settings.get('MAIL_USE_TLS', False) == 'ENABLED' else False
            app.config['MAIL_USE_SSL'] = True if mail_settings.get('MAIL_USE_SSL', False) == 'ENABLED' else False
            app.config['MAIL_USERNAME'] = mail_settings.get('MAIL_USERNAME', '')
            app.config['MAIL_PASSWORD'] = mail_settings.get('MAIL_PASSWORD', '')
            app.config['MAIL_DEFAULT_SENDER'] = mail_settings.get('MAIL_SENDER', '')


def _is_registered(app):
    """Answers if the system has been registered or not

    :param app app:
    :return bool registered:
    """
    with app.app_context():
        registered = Settings.query.join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
            .filter(Settings.settings_name.like('REGISTRATION')).with_entities(SettingsValues.value).one_or_none()
        if registered is not None:
            return True if registered.value == 'DISABLED' else False
        else:
            return False


def _construct_app_id(app):
    """Constructs the APP_ID for U2F from the hostname found in /etc/hostname

    :param app:
    :return:
    """
    with open('/etc/hostname', 'r') as f:
        hostname = f.readline().rstrip()
        app.config['SITE_DOMAIN'] = 'https://' + hostname + '.local'


def create_app():
    """Create Flask app.

    :return app: app - Flask Application
    """
    # Create application
    config = load_config()
    app = Flask(__name__)
    app.config.from_object(config)  # Loads configuration from settings

    # Check for python version. Using version 3.5 or higher
    if sys.version_info[:3] < app.config.get('REQUIRED_PYTHON_VER'):
        print("Monitor requires at least Python {}.{}.{}".format(*app.config.get('REQUIRED_PYTHON_VER')))
        sys.exit(1)

    # Set the mode of the server
    if not hasattr(app, 'production'):
        app.production = not app.debug and not app.testing

    # Over-ride existing template search directories
    my_loader = ChoiceLoader([
        app.jinja_loader,
        FileSystemLoader([
            os.path.join(app.config.get('PROJECT_PATH'), 'modislock_webservice/macros'),
            os.path.join(app.config.get('PROJECT_PATH'), 'modislock_webservice/pages')
        ])
    ])

    app.jinja_loader = my_loader

    # Makes /pages now available on <server>/pages
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/pages': os.path.join(app.config.get('PROJECT_PATH'), 'modislock_webservice/pages')
    })

    # Proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

    """ Extensions """
    # Initialize the database
    db.init_app(app)

    def _testdb():
        try:
            with app.app_context():
                db.session.query("1").from_statement(text("SELECT 1")).all()
            return True
        except:
            return False

    while _testdb() is not True:
        app.logger.debug('Database not available, waiting..')
        sleep(2)

    marshmallow.init_app(app)

    # Adds journal to logger, will log to system journal
    app.logger.addHandler(journal.JournalHandler(SYSLOG_IDENTIFIER='modis-admin'))
    app.logger.setLevel(level=logging.DEBUG if app.debug else logging.INFO)
    app.logger.info('ModisLock Administration Started')
    debug_toolbar.init_app(app)

    # Security
    user_datastore = SQLAlchemyUserDatastore(db, User, None)
    security_ctx = security.init_app(app, user_datastore)
    csrf_protect.init_app(app)

    # Assets
    assets.init_app(app)
    html_min.init_app(app)
    assets.register(asset_bundles)

    # Cache
    cache.init_app(app)

    # Mail
    _load_mail_settings(app)
    mail.init_app(app)

    # Async
    celery.init_app(app)

    # API Resources
    rest_api.add_resource(UsersAPI, '/api/v1.0/user', endpoint='users')
    rest_api.add_resource(UserAPI, '/api/v1.0/user/<int:user_id>', endpoint='user')
    rest_api.add_resource(KeyAPI, '/api/v1.0/key/<int:user_id>', endpoint='key')
    rest_api.add_resource(EventAPI, '/api/v1.0/event/<int:user_id>', endpoint='events')
    rest_api.add_resource(UtilsAPI, '/api/v1.0/utils', endpoint='utils')
    rest_api.init_app(app)

    # Register routes
    if not _is_registered(app):
        from .controllers.registration.welcome import bp

        app.register_blueprint(bp)
    else:
        # Controllers
        from . import controllers

        for _module in _import_submodules_from_package(controllers):
            try:
                bp = getattr(_module, 'bp')
            except AttributeError:
                continue
            if bp and isinstance(bp, Blueprint):
                app.register_blueprint(bp)

    _construct_app_id(app)

    """Register HTTP error pages."""
    @app.errorhandler(403)
    def page_403(error):
        return render_template('403/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('500/500.html'), 500

    @app.errorhandler(CSRFError)
    def csrf_error(e):
        return redirect(url_for('security.login'))

    @security_ctx.send_mail_task
    def delay_security_email(msg):
        send_security_email.delay(subject=msg.subject, sender=str(msg.sender),
                                  recipients=msg.recipients, body=msg.body,
                                  html=msg.html)

    return app


__all__ = ['create_app']

