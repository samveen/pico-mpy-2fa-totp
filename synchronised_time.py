import time
import ntptime
import utime
import network
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
sta_if = network.WLAN(network.STA_IF)

# https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
def do_connect():
    if not sta_if.isconnected():
        lcd.putstr('Connecting to network...')
        time.sleep(0.5)
        lcd.clear()
        sta_if.active(True)
        sta_if.connect('<ssid>', '<key>')

        while not sta_if.isconnected():
            pass

    lcd.putstr('Connected\n' + sta_if.ifconfig()[0])
    time.sleep(0.5)
    lcd.clear()

def create_synchronised_time():
    ntptime.settime() # ntptime.py settime() does not cope with errors #7137 https://github.com/micropython/micropython/issues/7137
    lcd.putstr('Synchronised')
    time.sleep(0.5)
    lcd.clear()
    sta_if.active(False)
    lcd.putstr('Disconnecting')
    time.sleep(0.5)
    lcd.clear()
    
    def synchronised_time():
        return int(utime.time())
    
    return synchronised_time
    
