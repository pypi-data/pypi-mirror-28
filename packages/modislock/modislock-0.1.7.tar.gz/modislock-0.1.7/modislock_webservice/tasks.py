# coding: utf-8

from .extensions import celery, mail
from flask_mail import Message, BadHeaderError
from subprocess import Popen, PIPE
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        # sentrycli.captureException(exc)
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        # sentrycli.captureException(exc)
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@celery.task(bind=True)
def upgrade_modislock(self, package, version=None):
    logger.info('Package: {} Version: {}'.format(package, version))

    if not isinstance(package, (str, bytearray)):
        return {'data': 'Bad package type:'.format(type(package))}
    if version:
        if not isinstance(version, (str, bytearray)):
            return {'data': 'Bad version'}

    args = ['pip3', 'install', '--upgrade', package]
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    message_cnt = 0

    while True:
        output = process.stdout.readline()

        if output and output != '':
            self.update_state(state='PROGRESS',
                              meta={'count': message_cnt,
                                    'message': output.decode('utf-8').strip()})
            message_cnt += 1
        if process.poll() is not None:
            break

    return {'count': message_cnt, 'message': 'Completed'}


@celery.task()
def send_async_command(cmd):
    logger.info('Commands: {}'.format(cmd))
    cmd = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, error = cmd.communicate()

    return {"result": stdout.decode('utf-8'), "error": error.decode('utf-8')}


@celery.task()
def send_async_email(msg_dict):
    msg = Message()
    msg.__dict__.update(msg_dict)
    mail.send(msg)


@celery.task(bind=True, max_retries=3, soft_time_limit=5)
def send_security_email(self, **kwargs):
    try:
        mail.send(Message(**kwargs))
    except Exception as e:
        self.retry(countdown=10, exc=e)


__all__ = ['send_security_email', 'send_async_command', 'send_async_email', 'upgrade_modislock']
