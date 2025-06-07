from wakeonlan import send_magic_packet
from flask import Flask, redirect, render_template, request, url_for
import sqlite3
import os
import getmac
import scapy
import re

# SERVER_DIR_PATH = "/media/server/"
SERVER_DIR_PATH = "./"
DATABASE_FILENAME = "database.sqlite"
DB_WAKEONLAN_TABLE = "WAKEONLAN"

app = Flask(__name__)

def is_mac_address_valid(mac_addr):
    return re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_addr.lower())

@app.route('/')
def index():
    pc_mac_addresses = []
    with sqlite3.connect(SERVER_DIR_PATH + DATABASE_FILENAME) as database:
            cursor = database.cursor()
            cursor.execute(F"SELECT pc_name, mac_addr FROM {DB_WAKEONLAN_TABLE}")
            pc_mac_addresses = cursor.fetchall()
            print("database query: ", pc_mac_addresses)
            tmp = {}
            for item in pc_mac_addresses:
                tmp[item[0]] = item[1]

    return render_template('index.html', pc_list=pc_mac_addresses)

@app.route('/add_pc', methods=['GET', 'POST'])
def add_pc():
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']
        pc_name = request.form['PC_NAME']

        if not is_mac_address_valid(mac_addr) or len(pc_name.strip()) == 0:
            return "mac address or pc name not valid"

        print("request to send wol for: ", pc_name, " ", mac_addr)

        with sqlite3.connect(SERVER_DIR_PATH + DATABASE_FILENAME) as database:
            database.execute(F"INSERT INTO {DB_WAKEONLAN_TABLE} (pc_name, mac_addr) VALUES(?, ?)", (pc_name, mac_addr))
            database.commit()

        send_magic_packet(mac_addr)
    return render_template('add_pc.html')

@app.route('/send_wol_packet', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        mac_addr = request.form['MAC_ADDR']

        print("request to send wol for: ", mac_addr)
        send_magic_packet(mac_addr)
    return redirect(url_for('index'))

# @app.route('/send_wol_packet', methods=['GET'])
# def send_wol():
#     send_magic_packet(PC_MAC_ADDRESSES)
#     print(F"sending WOL to {PC_MAC_ADDRESSES}")
#     return F"sending WOL to {PC_MAC_ADDRESSES}"

def run():
    clean_starup = not os.path.exists(SERVER_DIR_PATH + DATABASE_FILENAME)
    if clean_starup:
        print("no database found - creating ", SERVER_DIR_PATH + DATABASE_FILENAME)

    with sqlite3.connect(SERVER_DIR_PATH + DATABASE_FILENAME) as database:
        database.execute(F"CREATE TABLE IF NOT EXISTS {DB_WAKEONLAN_TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT, pc_name TEXT, mac_addr TEXT);")
        database.commit()

        app.run(host='0.0.0.0', port='5001')

run()