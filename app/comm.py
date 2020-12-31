import serial
from app import utils
import time

class UARTInterface():
    def __init__(self, port: str, baud: int):
        #self.conn = serial.Serial(port=port, baudrate=baud)
        self.conn = serial.serial_for_url(f"spy:///{port}?file=spy.txt", baudrate=baud, timeout=1)

        # Allow Arduino time to reset after UART init
        time.sleep(2)

    def write(self, data: str):
        print(data)
        self.__write_bytes(utils.str_to_bytes(data))

    def read(self) -> str:
        data = utils.bytes_to_str(self.__read_bytes())
        return data

    def __write_bytes(self, data: bytes):
        self.conn.write(data)

    def __read_bytes(self) -> bytes:
        #data = self.conn.read_until("\n", 50)
        data = self.conn.readline()
        return data

    def close(self):
        self.conn.close()