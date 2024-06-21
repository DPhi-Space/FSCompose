# Power Control API Documentation
## Overview

The pdb_fun.py stub provides an interface for controlling power to specific ports. This stub is designed to be used for standalone development of containers. When developping and testing with DPhi Space FSCompose, do not include this stub as the PDB API is already provided. This stub version returns the same responses as the real PDB API in case of no error. 

This API is meant to be used by Docker Containers thath will be running running Python to communicate with their Payloads. 



# Initialization

First, you need to create an instance of the PowerControl class. This instance will allow you to interact with the power control API.

```python
    from pdb_fun import PowerControl

    power_control = PowerControl()
```

##  API Methods
### get_power

*Description*

Retrieve the current power state of a specific port.

*Parameters*


- **port** (int): The port number to query (valid range: 0 to 3).
    

*Returns* 

- A dictionary containing the power state of the requested port, e.g., *{"power": True}*.

*Usage*

```python
    response = power_control.get_power(port=1)
    print(response)  # Output: {"power": False}
```

### set_power
*Description*

Set the power state of a specific port.

*Parameters*

- **port** (int): The port number to set the power state (valid range: 0 to 3).
- **power_opt** (bool): The desired power state (True for on, False for off).

*Returns*

- None

*Usage*

python

```python
    power_control.set_power(port=1, power_opt=True)
```


### get_time_on

*Description*

Retrieve the total time that the power ports have been switched on.

*Parameters*

- None


*Returns*

- A dictionary containing the total time the power ports have been switched on, e.g., *{"time_on": 3600.0}*.

*Usage*

```python
    response = power_control.get_time_on()
    print(response)  # Output: {"time_on": 3600.0}
```

# Usage Example

Below is an example of how to use the PowerControl API to control power to the ports:

```python
    from pdb_fun import PowerControl
    import time

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

```