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

SERVER_DIR_PATH = '/server/config/'
# SERVER_DIR_PATH = "./"
DATABASE_FILENAME = 'database.sqlite'
NETWORK_SUBNET = '192.168.0.0/24'

app = Flask(__name__)
persistant = Persistant(SERVER_DIR_PATH + DATABASE_FILENAME)


@app.route('/')
def index() -> str | Any:
    return render_template('index.html', pc_list=persistant.get_pc_mac_addresses())


@app.route('/add_pc', methods=['GET', 'POST'])
def add_pc() -> str | Any:
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']
        pc_name = request.form['PC_NAME']

        if not persistant.add_pc_mac_addr(pc_name, mac_addr):
            return 'mac address or pc name not valid'

    device_list = scan_network_ip_addresses(NETWORK_SUBNET)
    print(F'device_list: {device_list}')
    return render_template('add_pc.html', mac_adresses=device_list)


@app.route('/delete_pc', methods=['GET', 'POST'])
def delete_pc() -> str | Any:
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']

        persistant.delete_pc_mac_addresses(mac_addr)
    return render_template('delete_pc.html', pc_list=persistant.get_pc_mac_addresses())


@app.route('/send_wol_packet', methods=['GET', 'POST'])
def send() -> Response:
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']

        print('request to send wol for: ', mac_addr)
        send_magic_packet(mac_addr)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
