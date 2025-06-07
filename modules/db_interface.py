import os
import sqlite3
import re

def is_mac_address_valid(mac_addr):
    return re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_addr.lower())

class Persistant:
    def __init__(self, database_path):
        self.DB_WAKEONLAN_TABLE = "WAKEONLAN"
        self.database_path = database_path

        clean_starup = not os.path.exists(self.database_path)
        if clean_starup:
            print("no database found - creating ", self.database_path)

        with sqlite3.connect(self.database_path) as database:
            database.execute(F"CREATE TABLE IF NOT EXISTS {self.DB_WAKEONLAN_TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT, pc_name TEXT, mac_addr TEXT);")
            database.commit()
    
    def get_pc_mac_addresses(self) -> dict:
        with sqlite3.connect(self.database_path) as database:
            cursor = database.cursor()
            cursor.execute(F"SELECT pc_name, mac_addr FROM {self.DB_WAKEONLAN_TABLE}")
            pc_mac_addresses = cursor.fetchall()

            tmp = {}
            for item in pc_mac_addresses:
                tmp[item[0]] = item[1]

            return tmp

    def add_pc_mac_addr(self, pc_name, mac_addr) -> bool:
        if not is_mac_address_valid(mac_addr) or len(pc_name.strip()) == 0:
            return False

        with sqlite3.connect(self.database_path) as database:
            database.execute(F"INSERT INTO {self.DB_WAKEONLAN_TABLE} (pc_name, mac_addr) VALUES(?, ?)", (pc_name, mac_addr))
            database.commit()

            print(F"saved {pc_name} - {mac_addr} to db")
            return True
    
    def delete_pc_mac_addresses(self, mac_addr):
        with sqlite3.connect(self.database_path) as database:
            try:
                delete_query = F"DELETE FROM {self.DB_WAKEONLAN_TABLE} WHERE mac_addr = ?"
                database.execute(delete_query, (mac_addr,))
                database.commit()
            except sqlite3.Error as error:
                print("SQL-Error:", error)
                return False

            print(F"deleted {mac_addr} to db")
            return True