"""
Description: DPhi Space GPIO Library v1.0
Author:      Michael Linder, DPhi Space
"""

import json
import requests


# open config
with open('config.json', 'r') as f:
    config = json.load(f)


API_BASE_URL = config['api']['base_url']

class GPIO:
    def __init__(self, bank_id, gpio_id):
        self.bank_id = bank_id
        self.gpio_id = gpio_id

    def set_value(self, value):
        url = API_BASE_URL + f"gpio/{self.bank_id}/{self.gpio_id}"
        data = {
            'value': value
        }
        response = requests.put(url, json=data)

    def get_value(self):
        value = requests.get(API_BASE_URL + f"gpio/{self.bank_id}/{self.gpio_id}").json()['value']
        return value

    def set_direction(self, direction):
        url = API_BASE_URL + f"gpio/{self.bank_id}/{self.gpio_id}"
        data = {
            'direction': direction
        }
        response = requests.put(url, json=data)

    def get_direction(self):
        direction = requests.get(API_BASE_URL + f"gpio/{self.bank_id}/{self.gpio_id}").json()['direction']
        return direction
    
    def debug_set_value(self, value):
        url = API_BASE_URL + f"gpio_debug/{self.bank_id}/{self.gpio_id}"
        data = {
            'value': value
        }
        response = requests.put(url, json=data)
        return response


class GPIO_Bank():

    def __init__(self, bank_id):
        bank_config = config['gpio_banks'][str(bank_id)]
        self.name = bank_config['name']
        self.num_gpios = bank_config['num_gpios']
        self.bank_id = bank_id
        self.gpios = []
        for gpio_id in range(self.num_gpios):
            self.gpios.append(GPIO(bank_id, gpio_id))

    def get_gpio_by_id(self, id):
        return self.gpios[id]
    
    def get_info(self):
        url = API_BASE_URL + f"gpio_banks/{self.bank_id}/info"
        response = requests.get(url)
        print(response)
        return response.json()