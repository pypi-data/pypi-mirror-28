# coding: utf-8

# Flask
from flask import render_template, Blueprint, request, current_app
from flask_security import login_required
from ..forms import SettingsNetworkForm

# Networking
from ..utils.pynetlinux import ifconfig, route
import debinterface
import dns.resolver

# Nginx
import nginx

# System
from ..tasks import send_async_command


bp = Blueprint('settings_network', __name__)


def _save_hostname(old_name, new_name):
    """Saves hostname, reconfigures nginx server, and re-initializes the app APP_ID

    :param str old_name:
    :param str new_name:
    :return:
    """
    with open('/etc/hostname', 'r') as f:
        s = f.read()

    if old_name in s:
        key_args = ['openssl', 'genrsa', '-out', '/var/www/modislock.key', '2048']
        cert_args = ['openssl', 'req', '-new', '-x509', '-key', '/var/www/modislock.key', '-out',
                     '/var/www/modislock.cert', '-days', '3650', '-subj']

        # Safely write the changed content, if found in the file
        with open('/etc/hostname', 'w') as f:
            s = s.replace(old_name, new_name)
            f.write(s)
        new_server_name = new_name + '.local'
        current_app.config['SITE_DOMAIN'] = 'https://' + new_server_name
        modis = nginx.loadf('/etc/nginx/sites-available/admin_site')
        modis.filter('Server')[0].filter('Key', 'server_name')[0].value = new_server_name
        modis.filter('Server')[1].filter('Key', 'server_name')[0].value = new_server_name
        nginx.dumpf(modis, '/etc/nginx/sites-available/admin_site')
        # Generate the key
        send_async_command.apply_async(args=[key_args])

        # Generate certificate
        cert_args.append('/CN=' + new_server_name)
        send_async_command.apply_async(args=[cert_args])


def _save_network_settings(form):
    """Saves network settings

    :param form form:
    :returns bool: result of save
    """
    old_settings = _get_network_settings()
    new_settings = dict()
    result = False

    # new_settings['hostname'] = form.host_name.data
    new_settings['dhcp_mode'] = form.dhcp_mode.data

    if not new_settings['dhcp_mode']:
        new_settings['ip_address'] = form.ip_address.data
        new_settings['subnet'] = str(_mask_to_slash(form.sub_address.data))
        new_settings['gateway'] = form.gw_address.data
        new_settings['pri_dns'] = form.dns1_address.data
        new_settings['sec_dns'] = form.dns2_address.data

    interface = ifconfig.Interface(bytes(route.get_default_if(), 'utf-8'))

    try:
        net_interface = debinterface.Interfaces()
    except FileNotFoundError:
        current_app.logger.debug('Network interface file not found')
    else:
        adapter = net_interface.getAdapter(interface.name.decode("utf-8"))

        if new_settings['hostname'] != old_settings['hostname']:
            _save_hostname(old_settings['host_name'], new_settings['hostname'])

        if new_settings['dhcp_mode'] != old_settings['dhcp_mode']:
            current_app.logger.debug('Writing network settings')

            if new_settings['dhcp_mode']:
                adapter.setAddressSource('dhcp')
            else:
                adapter.setAddressSource('static')

                try:
                    adapter.setAddress(new_settings['ip_address'])
                    adapter.setNetmask(new_settings['subnet'])
                    adapter.setGateway(new_settings['gateway'])
                    adapter.setDnsNameservers(new_settings['pri_dns'])
                except ValueError:
                    current_app.logger.debug('Network values were incompatible')
                    return result

            try:
                current_app.logger.debug('Write new settings to file')
                net_interface.writeInterfaces()
            except:
                current_app.logger.debug('Could not write settings to file')
            else:
                result = True
        else:
            current_app.logger.debug('Existing network settings have not changed')
            result = True
    return result


def _get_network_settings():
    """Retrieves network settings from multiple sources and formats for form output

    :return dict network_data:
    """
    dhcp_mode = True
    pri_dns = '8.8.8.8'
    sec_dns = '8.8.4.4'

    interface = ifconfig.Interface(bytes(route.get_default_if(), 'utf-8'))

    try:
        adapter = debinterface.Interfaces().getAdapter(interface.name.decode("utf-8"))
    except FileNotFoundError:
        adapter = None
    if adapter is not None:
        options = adapter.export()
        dhcp_mode = True if (options['source'] == 'manual' or options['source'] == 'dhcp') else False

        if dhcp_mode:
            res = dns.resolver.Resolver()

            try:
                pri_dns = res.nameservers[0]
                sec_dns = res.nameservers[1]
            except IndexError:
                current_app.logger.debug('Unabled to reader DNS server addresses in network settings')
        else:
            pri_dns = options.get('dns-nameservers')
            sec_dns = options.get('nameserver2', '8.8.8.8')

    with open('/etc/hostname', 'r') as f:
        hostname = f.readline().rstrip()

    data = {
        'hostname': hostname,
        'dhcp_mode': dhcp_mode,
        'ip_address': interface.get_ip(),
        'subnet': _slash_to_mask(interface.get_netmask()),
        'gateway': route.get_default_gw(),
        'pri_dns': pri_dns,
        'sec_dns': sec_dns,
        'mac_address': interface.get_mac()
    }

    return data


def _mask_to_slash(mask):
    """Converts IP4 format subnet mask text string to linux netmask integer value
    ex) 255.255.255.0 => 24  (24 ones followed by 8 zeros to mark first 24 bits in a 32 bit field)
    
    :param str mask:
    :return int:
    """
    try:
        ip = mask.split('.')
        s_sum = 0

        for i in ip:
            s = str(format(int(i), 'b'))
            s_cnt = s.count('1')
            s_sum += s_cnt
    except AttributeError:
        return 24
    else:
        return s_sum


def _slash_to_mask(slash):
    """Converts linux subnet mask integer value to IP4 format text
    ex) 23 => 255.255.254.000 

    :param int slash:
    :return str:
    """

    mask_bits = []

    for i in range(32, 0, -1):
        if i > 32 - slash:
            mask_bits.append('1')
        else:
            mask_bits.append('0')

    # print(''.join(mask_bits))
    mask_txt = str(int(''.join(mask_bits[0:8]), 2))+'.'+str(int(''.join(mask_bits[8:16]), 2))+'.'+str(int(''.join(mask_bits[16:24]), 2))+'.'+str(int(''.join(mask_bits[24:32]), 2))

    return mask_txt


@bp.route('/settings/network', methods=['GET', 'POST'])
@login_required
def network_settings():
    """Endpoint for network settings page

    :return html settings_network:
    """
    form = SettingsNetworkForm()
    mac_address = ''
    save_result = False

    if request.method == 'POST':
        if form.validate_on_submit():
            save_result = _save_network_settings(form)

    try:
        settings = _get_network_settings()
    except ValueError as e:
        current_app.logger.error(e)
    else:
        form.host_name.data = settings.get('hostname', '')
        form.dhcp_mode.data = settings.get('dhcp_mode', 'True')
        form.ip_address.data = settings.get('ip_address', '')
        form.sub_address.data = settings.get('subnet', '')
        form.gw_address.data = settings.get('gateway', '')
        form.dns1_address.data = settings.get('pri_dns', '')
        form.dns2_address.data = settings.get('sec_dns', '')
        mac_address = settings.get('mac_address', '')

    return render_template('settings_network/settings_network.html', form=form, mac_address=mac_address,
                           save_result=save_result)
