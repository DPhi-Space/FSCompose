from gpio_fun import GPIO_Bank

bank = GPIO_Bank(0)

bank_info = bank.get_info()
print(f"Connected to Bank '{bank_info['name']}' with {bank_info['gpios']} GPIOs")
print("Bank Description: " + bank_info['description'])

bank.get_gpio_by_id(1).set_value(1)
bank.get_gpio_by_id(1).set_direction('output')

bank.get_gpio_by_id(2).set_value(0)
bank.get_gpio_by_id(2).set_direction('output')

bank.get_gpio_by_id(3).set_direction('input')
bank.get_gpio_by_id(3).debug_set_value(1)

val = bank.get_gpio_by_id(1).get_value()
d = bank.get_gpio_by_id(1).get_direction()
print(f"GPIO 1: Value: {val}, Direction: {d} --- expected 1 and output")

val = bank.get_gpio_by_id(2).get_value()
d = bank.get_gpio_by_id(2).get_direction()
print(f"GPIO 2: Value: {val}, Direction: {d} --- expected 0 and output")

val = bank.get_gpio_by_id(3).get_value()
d = bank.get_gpio_by_id(3).get_direction()
print(f"GPIO 3: Value: {val}, Direction: {d} --- expected 1 and input")

bank.get_gpio_by_id(3).debug_set_value(0)

val = bank.get_gpio_by_id(3).get_value()
print(f"GPIO 3: Value: {val}, Direction: {d} --- expected 0 and input")





