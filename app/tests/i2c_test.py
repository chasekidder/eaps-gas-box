import serial
import time

device_addr = bytearray.fromhex("68")
register_addr = bytearray.fromhex("08")

# bytes to read, num_data_bytes, cmd, h_reg_addr, l_reg_addr, checksum
data_bytes = bytearray.fromhex("04 04 22 00 08 2A")

with serial.serial_for_url("spy:////dev/ttyACM0?file=spy.txt", baudrate=9600, timeout=1) as s:

    time.sleep(2)

    data = bytearray(b"<I2C|R\x68")
    data.extend(data_bytes)
    data.extend(bytearray(b">"))
    print("Sending: " + str(data))
    s.write(data)
    
    for i in range(20):
        print(s.readline())


