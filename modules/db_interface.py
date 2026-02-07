import os
import re
import sqlite3


def is_mac_address_valid(mac_addr: str) -> re.Match[str] | None:
    return re.match('[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$', mac_addr.lower())


class Persistant:
    def __init__(self, database_path: str):
        self._db_wakeonlan_table = 'WAKEONLAN'
        self._db_application_settings_table = 'APP_SETTINGS'
        self.database_path = database_path

        clean_starup = not os.path.exists(self.database_path)
        if clean_starup:
            print('no database found - creating ', self.database_path)
            self._set_db_version(0)

        self._migrate_db_if_needed()

    def get_pc_mac_addresses(self) -> dict[str, str]:
        with sqlite3.connect(self.database_path) as database:
            cursor = database.cursor()
            cursor.execute(F'SELECT pc_name, mac_addr FROM {self._db_wakeonlan_table}')
            pc_mac_addresses = cursor.fetchall()

            tmp = {}
            for item in pc_mac_addresses:
                tmp[item[0]] = item[1]

            return tmp

    def add_pc_mac_addr(self, pc_name: str, mac_addr: str) -> bool:
        if not is_mac_address_valid(mac_addr) or len(pc_name.strip()) == 0:
            return False

        with sqlite3.connect(self.database_path) as database:
            database.execute(
                F'INSERT INTO {self._db_wakeonlan_table} (pc_name, mac_addr) VALUES(?, ?)',
                (pc_name, mac_addr),
            )
            database.commit()

            print(F'saved {pc_name} - {mac_addr} to db')
            return True

    def delete_pc_mac_addresses(self, mac_addr: str) -> bool:
        with sqlite3.connect(self.database_path) as database:
            try:
                delete_query = F'DELETE FROM {self._db_wakeonlan_table} WHERE mac_addr = ?'
                database.execute(delete_query, (mac_addr,))
                database.commit()
            except sqlite3.Error as error:
                print('SQL-Error:', error)
                return False

            print(F'deleted {mac_addr} to db')
            return True

    def get_db_version(self) -> int | None:
        with sqlite3.connect(self.database_path) as database:
            version = database.execute('PRAGMA user_version').fetchone()
            return version[0] if version else None

    def _set_db_version(self, version: int) -> bool:
        self._execute_single_command(F'PRAGMA user_version = {version}')
        return True

    def get_app_settings(self, setting_key: str) -> str | None:
        with sqlite3.connect(self.database_path) as database:
            row = database.execute(
                F"""SELECT setting_value FROM {self._db_application_settings_table}
                WHERE setting_key = '{setting_key}'""",
            ).fetchone()
            return row[0] if row else None

    def set_app_settings(self, setting_key: str, setting_value: str) -> None:
        self._execute_single_command(
            F"""UPDATE {self._db_application_settings_table}
            SET setting_value = '{setting_value}'
            WHERE setting_key = '{setting_key}'""",
        )

    def _execute_single_command(self, sql: str) -> None:
        with sqlite3.connect(self.database_path) as database:
            database.execute(sql)
            database.commit()

    def _migrate_db_if_needed(self) -> None:
        if self.get_db_version() == 0:
            print('migration DB from 0 to 1')
            self._execute_single_command(
                F"""CREATE TABLE IF NOT EXISTS {self._db_wakeonlan_table}
                (id INTEGER PRIMARY KEY AUTOINCREMENT, pc_name TEXT, mac_addr TEXT);""",
            )
            self._execute_single_command(
                F"""CREATE TABLE IF NOT EXISTS {self._db_application_settings_table} (
                    setting_key TEXT PRIMARY KEY,
                    setting_value TEXT
                    );""",
            )
            self._set_db_version(1)
        if self.get_db_version() == 1:
            print('migration DB from 1 to 2')
            self._execute_single_command(
                F"""INSERT OR IGNORE INTO {self._db_application_settings_table}
                (setting_key, setting_value) VALUES ('app_version', 'v1.1.0');""",
            )
            self._execute_single_command(
                F"""INSERT OR IGNORE INTO {self._db_application_settings_table}
                (setting_key, setting_value) VALUES ('operating_system', 'linux');""",
            )
            self._set_db_version(2)
        if self.get_db_version() == 2:
            print('migration DB from 2 to 3')
            self._execute_single_command(
                F"""INSERT OR IGNORE INTO {self._db_application_settings_table}
                (setting_key, setting_value) VALUES ('network_subnet', '192.168.0.0/24');""",
            )
            self._execute_single_command(
                F"""UPDATE {self._db_application_settings_table}
                SET setting_value = 'v1.2.0' WHERE setting_key = 'app_version'""",
            )
            self._set_db_version(3)
