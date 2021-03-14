import sqlite3
import os
import io

from config import Config

CONFIG = Config("config.ini")

DEFAULT_PATH = os.path.join(CONFIG.PATH, "database.sqlite3")
DEFAULT_BACKUP_PATH = DEFAULT_PATH + ".sql"

class Database():
    def __init__(self, path:str = DEFAULT_PATH):
        if (os.path.exists(path)):
            self.con = sqlite3.connect(path)
        else:
            self.con = sqlite3.connect(path)
            self.con.execute("""CREATE TABLE "measurements" (
                "id"	INTEGER,
                "sensor"	TEXT NOT NULL,
                "timestamp"	TEXT NOT NULL,
                "type"	TEXT NOT NULL,
                "value"	REAL NOT NULL,
                "unit"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )""")

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
                print(measurement)
                self.curs.execute(sql_insert, (sensor, measurement["timestamp"],
                    measurement["type"], measurement["value"], measurement["unit"]))
