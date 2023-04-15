import time
import ntptime
import utime
import network

sta_if = network.WLAN(network.STA_IF)

# https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
def do_connect(lcd):
    if not sta_if.isconnected():
        lcd.text('Connecting to network...',0,0,lcd.white); lcd.show()
        time.sleep(0.5)
        lcd.clear()
        sta_if.active(True)
        sta_if.connect('SSID', 'Passphrase')

        while not sta_if.isconnected():
            pass

    lcd.text('Connected\n' + sta_if.ifconfig()[0],0,0,lcd.white);lcd.show()
    time.sleep_ms(1000)
    lcd.clear()

def create_synchronised_time(lcd):
    ntptime.settime() # ntptime.py settime() does not cope with errors #7137 https://github.com/micropython/micropython/issues/7137
    lcd.text('Synchronised',0,0,lcd.white); lcd.show()
    time.sleep_ms(500)
    lcd.clear()
    sta_if.active(False)
    lcd.text('Disconnecting',0,0,lcd.white); lcd.show()
    time.sleep_ms(500)
    lcd.clear()
    
    def synchronised_time():
        return int(utime.time())
    
    return synchronised_time
