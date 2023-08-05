# coding: utf-8
from .default import Config
import os


class DevelopmentConfig(Config):
    # App config
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24  # 1 Day
    WTF_CSRF_TIME_LIMIT = PERMANENT_SESSION_LIFETIME

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://modisweb:l3j4lkjlskjd@127.0.0.1/modislock"
    SQLALCHEMY_ECHO = False

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
    # Host string, used by fabric
    HOST_STRING = "root@172.104.135.149"

    SITE_DOMAIN = "http://127.0.0.1:5000"

    # Assets
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True

    MINIFY_PAGE = False

    # Celery
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
