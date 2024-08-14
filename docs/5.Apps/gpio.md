# GPIO API

This API allows to access to GPIOs. Note that there is no difference between local and remote GPIOs resulting in portable code.

## General

A GPIO is identified by his **bank** and **id**. Authentication (invisible to the user) is managed on a bank-level.
The API is implemented as a REST-API with a python wrapper. This document only documents the latter. Please reach out to DPhi Space in case you need functionalities exceeding this documentation.

## Python Wrapper

### Initialize the GPIOs

You can import the **gpio_fun** library and create a bank. A bank can be initialized using its id (zero in the example below). Please use bank 0 for development and store the bank id in a single variable to allow for easy reconfiguration later.

```python
    $ from gpio_fun import GPIO_Bank
    $ BANK_ID = 0
    $ bank = GPIO_Bank(BANK_ID)
```

You can get some basic information about the bank as shown below. This also checks the connection to the API.

```python
    $ bank_info = bank.get_info()
    $ print(f"Connected to Bank '{bank_info['name']}' with {bank_info['gpios']} GPIOs")
    $ print("Bank Description: " + bank_info['description'])
```

### Toggling GPIOs

The python wrapper exposes four functions to set and get gpio direction and value. The example below shows how to use them.

```python
# Set output GPIO
    $ bank.get_gpio_by_id(1).set_direction('output')
    $ bank.get_gpio_by_id(1).set_value(1)
    $
# Read input GPIO
    $ bank.get_gpio_by_id(2).set_direction('input')
    $ val = bank.get_gpio_by_id(2).get_value()
```

### Debugging

The API exposes a **debug_set_value** function which directly accesses the backend and sets the value of a GPIO defined as **input**. This can be used to simulate an outside event.

```python
# Read input GPIO
    $ bank.get_gpio_by_id(3).set_direction('input')
    $ bank.get_gpio_by_id(3).debug_set_value(1)
    $ val = bank.get_gpio_by_id(3).get_value() # val = 1
    $ bank.get_gpio_by_id(3).debug_set_value(0)
    $ val = bank.get_gpio_by_id(3).get_value() # val = 0
```

If you want to interact with hardware, we recommend you to directly modify the **GPIO** class in **gpio_func_custom.py**. This class must implement the functions shown in the skeleton below. Note that the debug_set_value function is not needed when interacting with hardware but shown for completeness.
You can then import **gpio_func_custom** instead of **gpio_func** to use your own GPIO implementation.

```python
class GPIO:
    def __init__(self, bank_id, gpio_id):
        self.bank_id = bank_id
        self.gpio_id = gpio_id

    def set_value(self, value):
        pass

    def get_value(self):
        pass

    def set_direction(self, direction):
        pass

    def get_direction(self):
        pass

    def debug_set_value(self, value):
        pass

```
