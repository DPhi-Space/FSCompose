import time
from pdb_fun import PowerControl

if __name__ == "__main__":

    power = PowerControl()
    print("PDB Control Example")
    
    while True:
        power.set_power(True)
        print("Current power state : ", power.get_power())
        time.sleep(30)
        power.set_power(True)
        print("Current power state : ", power.get_power())
        time.sleep(30)
