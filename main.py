from typing import Any

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import url_for
from wakeonlan import send_magic_packet

from modules.db_interface import Persistant
from modules.scan_network import scan_network_ip_addresses
from modules.tools import is_valid_subnet

SERVER_DIR_PATH = '/server/config/'
# SERVER_DIR_PATH = './'
DATABASE_FILENAME = 'database.sqlite'
NETWORK_SUBNET = '192.168.0.0/24'

app = Flask(__name__)
persistant = Persistant(SERVER_DIR_PATH + DATABASE_FILENAME)


@app.route('/')
def index() -> str | Any:
    return render_template('index.html', pc_list=persistant.get_pc_mac_addresses())


@app.route('/add_pc', methods=['POST'])
def add_pc() -> str | Any:
    mac_addr = request.form['MAC_ADDR']
    pc_name = request.form['PC_NAME']

    if not persistant.add_pc_mac_addr(pc_name, mac_addr):
        return 'mac address or pc name not valid'
    return redirect('/settings')


@app.route('/delete_pc', methods=['POST'])
def delete_pc() -> str | Any:
    mac_addr = request.form['MAC_ADDR']

    persistant.delete_pc_mac_addresses(mac_addr)
    return redirect('/settings')


@app.route('/update_subnet', methods=['POST'])
def update_subnet() -> str | Any:
    global NETWORK_SUBNET  # pylint: disable=global-statement

    valid_subnet, subnet_ip_str = is_valid_subnet(request.form['SUBNET'])

    if valid_subnet:
        persistant.set_app_settings('network_subnet', subnet_ip_str)
        NETWORK_SUBNET = subnet_ip_str if subnet_ip_str else NETWORK_SUBNET
        return redirect('/settings')
    return 'invalid subnet'


@app.route('/settings', methods=['GET'])
def settings_page() -> str | Any:
    device_list = scan_network_ip_addresses(NETWORK_SUBNET)
    return render_template(
        'settings.html', pc_list=persistant.get_pc_mac_addresses(),
        mac_adresses=device_list, subnet=NETWORK_SUBNET,
    )


@app.route('/send_wol_packet', methods=['GET', 'POST'])
def send() -> Response:
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']

        print('request to send wol for: ', mac_addr)
        send_magic_packet(mac_addr)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # persistant._set_db_version(0)
    subnet = persistant.get_app_settings('network_subnet')
    NETWORK_SUBNET = subnet if subnet else NETWORK_SUBNET

    print(F"App Version: {persistant.get_app_settings('app_version')}")
    print(F"Operating System: {persistant.get_app_settings('operating_system')}")
    print(F'DB Version: {persistant.get_db_version()}')
    print(F'Network Subnet: {NETWORK_SUBNET}')
    app.run(host='0.0.0.0', port='5001')
