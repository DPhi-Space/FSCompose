import serial
import time 

ser = serial.Serial("/dev/ttyACM0", 115200)
packet = bytearray()

for i in range(0x00, 0x07):
    packet.append(i)
    ser.write(packet)
    time.sleep(2)
