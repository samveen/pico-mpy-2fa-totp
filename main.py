from machine import I2C, Pin
import time
import json
from totp import totp
from pico_i2c_lcd import I2cLcd

from synchronised_time import create_synchronised_time, do_connect

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

button = Pin(16, Pin.IN, Pin.PULL_DOWN)
codes = json.loads(open("codes.json", "r").read())
selected_idx = 0

do_connect()

synchronised_time = create_synchronised_time()

while True:
    if button.value():
        selected_idx = (selected_idx + 1) % len(codes)

    code = codes[selected_idx]

    (password, expiry) = totp(synchronised_time(),
                              code['key'],
                              step_secs=code['step'],
                              digits=code['digits'])

    lcd.putstr(code['name'] + ' ' + str(expiry) + "\n" + password)
    time.sleep(0.5)
    lcd.clear()
