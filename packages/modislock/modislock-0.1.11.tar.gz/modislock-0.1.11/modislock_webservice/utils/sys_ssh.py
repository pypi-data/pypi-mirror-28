from subprocess import call, check_output, CalledProcessError
import re


def system_ssh(enabled=None):
    """Enable / Disable SSH or return active status

    :param bool enabled:
    :return bool:
    """
    args = ['systemctl', 'is-active', 'ssh']

    try:
        output = check_output(args)
    except CalledProcessError:
        return False

    output = re.search(r'(?P<enable>(?:active|inactive))', output)

    try:
        output = True if output.group('enable') == 'active' else False
    except IndexError:
        return False

    if enabled is None:
        return output
    else:
        if enabled:
            args = ['systemctl', 'enable', 'ssh', ';', 'systemctl', 'start', 'ssh']
        else:
            args = ['systemctl', 'stop', 'ssh', ';', 'systemctl', 'disable', 'ssh']

        try:
            result = call(args)
        except CalledProcessError:
            return False
        else:
            return True
