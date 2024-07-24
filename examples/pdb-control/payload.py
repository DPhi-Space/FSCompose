import time
from pdb_fun import PowerControl


if __name__ == "__main__":

    power = PowerControl()
    print("PDB Control Example")
    
    while True:
        power.set_power(0, True)
        print("Current power state port 0: ", power.get_power(0))
        time.sleep(2)
        power.set_power(0, False)
        print("Current power state port 0: ", power.get_power(0))
        time.sleep(2)
