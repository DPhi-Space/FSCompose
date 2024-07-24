import serial
import time

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
    ret = []
    while True:
        for i in range(0,10):
            ser.write(b'\x00\xB1')
            ret.append(ser.read(48))
            
            ser.write(b'\x00\xB2')
            ret.append(ser.read(48))
            
            ser.write(b'\x00\xB3')
            ret.append(ser.read(48))
            
            ser.write(b'\x00\xB4')
            ret.append(ser.read(48))
        time.sleep(30)
        
        for i in range(0,10):
            ser.write(b'\x00\xB1')
            ret.append(ser.read(48))
            
            ser.write(b'\x00\xB3')
            ret.append(ser.read(48))
            
            ser.write(b'\x00\xB2')
            ret.append(ser.read(48))
            
            ser.write(b'\x00\xB4')
            ret.append(ser.read(48))