from wakeonlan import send_magic_packet

PC_MAC_ADDRESS = "04:7c:16:80:a5:71"

if __name__ == "__main__":
    print(F"sending WOL to {PC_MAC_ADDRESS}")
    send_magic_packet(PC_MAC_ADDRESS)
