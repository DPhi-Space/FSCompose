import serial
import struct
import time
import shutil

OPCODE = 0
EXPECTED_MSG = 1

expected_bootup = 'Ready to receive commands'
commands = {
    'alive': [0x0000, 'I am Alive'],
    'temp': [0x00A1, 'Current Temperature: '],
    'unknown': [0xFFFF, 'Unknown command']
}

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

# Open log file
log_file = open('log.txt', 'w')

def print_and_log(message):
    print(message)
    log_file.write(message + '\n')

def send_command(op_code):
    command = struct.pack('>H', op_code)
    ser.write(command)
    time.sleep(0.1)
    response = ser.readline().decode('utf-8').strip()
    return response

def print_aligned(description, value, expected, equal=None):
    if equal is not None:
        msg = f"{description:30} | {value:50} | {expected:50} | {equal:10}"
    else:
        msg = f"{description:30} | {value:50} | {expected:50}"
    print_and_log(msg)

def run_test(command_name):
    op_code = commands[command_name][OPCODE]
    expected_msg = commands[command_name][EXPECTED_MSG]
    
    response = send_command(op_code)
    result = response.startswith(expected_msg)
    
    print_aligned(f'Response to {command_name.upper()}:', response, expected_msg, "Passed" if result else "Failed")
    
    return result

print_aligned('Waiting for bootup message...', '', '')
print_aligned("", "Received Message", "Expected Message")

bootup_msg = ser.readline().decode('utf-8').strip()
bootup_result = bootup_msg.startswith(expected_bootup)
print_aligned('Bootup message:', bootup_msg, expected_bootup, "Passed" if bootup_result else "Failed")

time.sleep(2)

test_results = []

for command_name in commands:
    test_passed = run_test(command_name)
    test_results.append(test_passed)

ser.close()

print_and_log("\nTest summary:")
print_and_log(f"{'Command':30} | {'Expected':50} | {'Result':10}")
print_and_log("-" * 95)

for command_name, result in zip(commands.keys(), test_results):
    expected_msg = commands[command_name][EXPECTED_MSG]
    result_str = "Passed" if result else "Failed"
    print_and_log(f"{command_name.upper():30} | {expected_msg:50} | {result_str:10}")
 
print_and_log("-" * 95)
print_and_log(f"Total tests     : {len(test_results)}")
print_and_log(f"Tests passed    : {test_results.count(True)}")
print_and_log(f"Tests failed    : {test_results.count(False)}")

# Close log file
log_file.close()

try:
    shutil.copy('log.txt', './data/log.txt')
except Exception as e:
    # Open the log file again to log the error
    with open('log.txt', 'a') as log_file:
        log_file.write(f"Data directory not mounted. Failed to move log.txt.\n")
    print(f"Data directory not mounted. Failed to move log.txt.")

while True:
    time.sleep(10)