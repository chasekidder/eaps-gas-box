import sqlite3
import os
import io

from config import Config

CONFIG = Config("config.ini")

DEFAULT_PATH = os.path.join(CONFIG.PATH, "database.sqlite3")
DEFAULT_BACKUP_PATH = DEFAULT_PATH + ".sql"

class Database():
    def __init__(self, path:str = DEFAULT_PATH):
        self.con = sqlite3.connect(path)
        self.curs = self.con.cursor()

    def backup(self, path:str = DEFAULT_BACKUP_PATH):
        with io.open(path, 'w') as f:
            for linha in self.con.iterdump():
                f.write('%s\n' % linha)
            print('Backup performed successfully.')

    def log_data(self, responses:dict):
        sql_insert = "INSERT INTO measurements (sensor, timestamp, type, value, unit) VALUES (?, ?, ?, ?, ?)"

        # Responses = {
        #           sensor1:[
        #               {
        #                   time:int,
        #                   type:str,
        #                   val:float,
        #                   unit:str
        #               }
        #           ], 
        #           sensor2:[
        #                   {},
        #                   {}
        #           ],
        #           ...
        #       }
        for sensor in responses: 
            for measurement in responses[sensor]:
                # Insert data into database
                print(sensor + responses[measurement]["timestamp"] + responses[measurement]["type"] + responses[measurement]["value"] + responses[measurement]["unit"])
                self.curs.execute(sql_insert, sensor, responses[measurement]["timestamp"],
                    responses[measurement]["type"], responses[measurement]["value"], responses[measurement]["unit"])
