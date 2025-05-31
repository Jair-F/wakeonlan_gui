from wakeonlan import send_magic_packet
from flask import Flask, render_template

PC_MAC_ADDRESS = "04:7c:16:80:a5:71"


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_wol_packet')
def send_wol():
    send_magic_packet(PC_MAC_ADDRESS)
    print(F"sending WOL to {PC_MAC_ADDRESS}")
    return F"sending WOL to {PC_MAC_ADDRESS}"

if __name__ == "__main__":
    app.run('0.0.0.0', '5001')
