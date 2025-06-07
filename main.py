from wakeonlan import send_magic_packet
from flask import Flask, redirect, render_template, request, url_for
from modules.db_interface import Persistant

# SERVER_DIR_PATH = "/media/server/"
SERVER_DIR_PATH = "./"
DATABASE_FILENAME = "database.sqlite"

app = Flask(__name__)
persistant = Persistant(SERVER_DIR_PATH + DATABASE_FILENAME)


@app.route('/')
def index():
    return render_template('index.html', pc_list=persistant.get_pc_mac_addresses())


@app.route('/add_pc', methods=['GET', 'POST'])
def add_pc():
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']
        pc_name = request.form['PC_NAME']

        if not persistant.add_pc_mac_addr(pc_name, mac_addr):
            return "mac address or pc name not valid"

    return render_template('add_pc.html')


@app.route('/delete_pc', methods=['GET', 'POST'])
def delete_pc():
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']

        persistant.delete_pc_mac_addresses(mac_addr)
    return render_template('delete_pc.html', pc_list=persistant.get_pc_mac_addresses())


@app.route('/send_wol_packet', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']

        print("request to send wol for: ", mac_addr)
        send_magic_packet(mac_addr)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001')
