import serial
import shutil
import time
import numpy
import datetime
import matplotlib.pyplot as plt
from pdb_fun import PowerControl

# Serial port configuration
SERIAL_PORT = '/dev/ttymxc2'  # Replace with your Arduino's serial port
BAUD_RATE = 115200
TIMEOUT = 1

# Initialize the serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
time.sleep(2)  # Give some time for the connection to establish

def send_command(command):
    """Send a command to the Arduino and wait for the response."""
    ser.write(bytes([command]))

def read_sensor_value(count, delay):
    with open('sensor_data.txt', 'a') as file:
        for i in range(count):
            try:
                send_command(0x01)  
                line = ser.readline().decode('utf-8').strip()
                sensor_value = int(line)
                file.write(f"{time.time()} {sensor_value}\n")
                time.sleep(delay)
            except ValueError:
                print("Received invalid data")

def run_color_wipe():
    send_command(0x02)
    print("Running color wipe animation...")

def run_theater_chase():
    send_command(0x03)
    print("Running theater chase animation...")

def run_rainbow():
    send_command(0x04)
    print("Running rainbow cycle animation...")

def plot_data():
    with open('sensor_data.txt') as f:
        lines = [line.rstrip() for line in f]
    time_data = []
    sensor_data = []
    for l in lines:
        time_data.append(float(l.rsplit()[0]))
        sensor_data.append(int(l.rsplit()[1]))

    time_data = numpy.array(time_data) - time_data[0]
    
    plt.figure(figsize=(12,6))
    plt.plot(time_data, sensor_data, 'ro')
    plt.title("LDR value over time(s)")
    plt.xlabel('Time [s]')
    plt.ylabel('LDR Value')
    plt.grid()
    plt.savefig('data.png')
    
        
    
    
def main():
    PORT = 1
    ser.flush()
    power = PowerControl()
    power.set_power(PORT, True)
    time.sleep(5)
    try:
        read_sensor_value(30, 2)
        time.sleep(1)
        run_color_wipe()
        time.sleep(1)
        run_theater_chase()
        time.sleep(1)
        run_rainbow()
        time.sleep(1)
        plot_data()
        print("Exiting program...")
        power.set_power(PORT, False)

    finally:
        ser.close()
        print("Serial connection closed.")
    

if __name__ == "__main__":
    main()
    try:
        shutil.copy('sensor_data.txt', './data/sensor_data.txt')
        shutil.copy('data.png', './data/data.png')
    except Exception as e:
        with open('sensor_data.txt', 'a') as log_file:
            log_file.write(f"Data directory not mounted. Failed to move sensor_data.txt.\n")
        print(f"Data directory not mounted. Failed to move sensor_data.txt.")
