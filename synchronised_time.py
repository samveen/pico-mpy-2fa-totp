import machine
import ntptime
import utime
import network
import json

WiFiSecrets=json.loads(open("WifiSecrets.json", "r").read())

ssid=None
passphrase=None

nic = network.WLAN(network.STA_IF)

# https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
def do_connect(lcd):
    global ssid
    global passphrase
    lcd.text('Scanning for known network...',0,0,0xffff); lcd.show()

    tries=3
    while tries > 0:
        nic.active(True)
        utime.sleep_ms(1500)
        for n in nic.scan():
            print(n[0],n[2],n[3],n[4])
            ssid=n[0].decode('utf-8')
            if ssid in WiFiSecrets:
                passphrase=WiFiSecrets[ssid]
                tries=0
                break
            else:
                ssid=None
        tries=tries-1
        utime.sleep_ms(1000)

    lcd.clear()

    if ssid is None:
        lcd.text('No known networks. Stopping.',0,0,0xffff); lcd.show()
        machine.deepsleep()

    if not nic.isconnected():
        lcd.text('Connecting to network...',0,0,0xffff); lcd.show()
        utime.sleep_ms(500)
        lcd.clear()
        nic.active(True)
        nic.connect(ssid,passphrase)

        while not nic.isconnected():
            pass

    lcd.text('Connected\n' + nic.ifconfig()[0],0,0,0xffff);lcd.show()
    utime.sleep_ms(1000)
    lcd.clear()

def create_synchronised_time(lcd):
    ntptime.settime() # ntptime.py settime() does not cope with errors #7137 https://github.com/micropython/micropython/issues/7137
    lcd.text('Synchronised',0,0,0xffff); lcd.show()
    utime.sleep_ms(500)
    lcd.clear()
    nic.active(False)
    lcd.text('Disconnecting',0,0,0xffff); lcd.show()
    utime.sleep_ms(500)
    lcd.clear()

    def synchronised_time():
        return int(utime.time())

    return synchronised_time
