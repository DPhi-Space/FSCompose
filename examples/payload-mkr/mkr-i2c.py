import smbus2
import time
from pdb_fun import PowerControl

I2C_ADDRESS = 0x00  # arduino's addresss

OPCODE_ALIVE = 0x0000
OPCODE_LED1 = 0x00B1
OPCODE_LED2 = 0x00B2
OPCODE_LED3 = 0x00B3
OPCODE_LED4 = 0x00B4


bus = smbus2.SMBus(4) # '1 refers to /dev/i2c-1 
power = PowerControl()
print("PDB Control Example")

def send_opcode(opcode):
    high_byte = (opcode >> 8) & 0xFF
    low_byte = opcode & 0xFF
    bus.write_i2c_block_data(I2C_ADDRESS, high_byte, [low_byte])

def main():
    
    power = PowerControl()
    power.set_power(3, True)
    time.sleep(5)
    try:
        print("Sending OPCODE_ALIVE...")
        send_opcode(OPCODE_ALIVE)
        time.sleep(1)  # Wait for a second

        print("Sending OPCODE_LED1...")
        send_opcode(OPCODE_LED1)
        time.sleep(1)

        print("Sending OPCODE_LED2...")
        send_opcode(OPCODE_LED2)
        time.sleep(1)

        print("Sending OPCODE_LED3...")
        send_opcode(OPCODE_LED3)
        time.sleep(1)

        print("Sending OPCODE_LED4...")
        send_opcode(OPCODE_LED4)
        time.sleep(1)
        

    except Exception as e:
        print(f"An error occurred: {e}")
        
    power.set_power(3, False)

if __name__ == "__main__":
    main()
