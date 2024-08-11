import smbus2
import time
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os

# I2C configuration
I2C_BUS = 2  # Bus number, often 1 for Raspberry Pi
I2C_ADDRESS = 0x00  # Replace with your Arduino's I2C address

# Initialize the I2C bus
bus = smbus2.SMBus(I2C_BUS)

def send_command(command):
    """Send a command to the Arduino over I2C."""
    bus.write_byte(I2C_ADDRESS, command)
    time.sleep(0.1)  # Short delay to ensure the command is processed

def read_sensor_value(count, delay):
    with open('sensor_data.txt', 'a') as file:
        for i in range(count):
            try:
                send_command(0x01)  
                time.sleep(0.1)  # Wait for Arduino to process and respond
                sensor_value = bus.read_byte(I2C_ADDRESS)
                file.write(f"{time.time()} {sensor_value}\n")
                time.sleep(delay)
            except Exception as e:
                print(f"Received invalid data: {e}")

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

    time_data = np.array(time_data) - time_data[0]
    
    plt.figure(figsize=(12,6))
    plt.plot(time_data, sensor_data, 'ro')
    plt.title("LDR value over time(s)")
    plt.xlabel('Time [s]')
    plt.ylabel('LDR Value')
    plt.grid()
    plt.savefig('data.png')
    
def main():
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

    finally:
        bus.close()
        print("I2C connection closed.")

if __name__ == "__main__":
    main()
    try:
        os.makedirs('./data', exist_ok=True)
        shutil.copy('sensor_data.txt', './data/sensor_data.txt')
        shutil.copy('data.png', './data/data.png')
    except Exception as e:
        with open('sensor_data.txt', 'a') as log_file:
            log_file.write(f"Data directory not mounted. Failed to move sensor_data.txt.\n")
        print(f"Data directory not mounted. Failed to move sensor_data.txt.")
