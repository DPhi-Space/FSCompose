"""
pdb_fun.py.stub

This is the stub version of the PDB API that will be provided
on board on Clustergate. It is intended for standalone development of containers. 
It returns the same responses the real PDB API would return in case of no error.

"""

import time
import requests

# each channel has 4 ports
NB_PORTS = 4

class PowerControl():
    def __init__(self):
        self.power          = [False] * NB_PORTS         
        self.last_time_on   = 0
        self.time_on        = 0                        # total time the power ports are switched on
                
    ##### Method Calls for Payload Containers
    
    # get the power state of the requested port
    def get_power(self, port, payload_id=0):
        if port >= 0 and port < NB_PORTS:
            return {"power": self.power[port]}
        else:
            print("[ERROR] Invalid Power Port Requested")
            return None

    # set the power state of a given port. No return value for now.
    def set_power(self, port, power_opt, payload_id=0):
        if port >= 0 and port < NB_PORTS:
            self.power[port] = power_opt
            if power_opt: 
                self.last_time_on   = time.time()
            else:
                self.time_on += time.time() - self.last_time_on   
        else:
            print("[ERROR] Invalid Power Port Requested")
            return None
            
    def get_time_on(self, payload_id=0):
        return {"time_on":self.time_on}
    
if __name__ == "__main__":
    # Initialize the PowerControl instance
    power_control = PowerControl()

    # Set port 1 to be powered on
    power_control.set_power(port=1, power_opt=True)

    # Get the power state of port 1
    power_state = power_control.get_power(port=1)
    print(f"Port 1 power state: {power_state['power']}")  # Output: Port 1 power state: True

    # Wait for some time (simulating the port being on)
    time.sleep(2)

    # Set port 1 to be powered off
    power_control.set_power(port=1, power_opt=False)

    # Get the total time the ports have been on
    total_time_on = power_control.get_time_on()
    print(f"Total time ports have been on: {total_time_on['time_on']} seconds")

    