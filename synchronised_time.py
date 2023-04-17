import machine
import ntptime
import utime
import network
import json
import cryptor

nic = network.WLAN(network.STA_IF)

# https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
def do_connect(lcd,key):
    ssid=None
    passphrase=None

    WiFiSecrets=json.loads(cryptor.decrypt("WifiSecrets.json.encoded",key))

    lcd.text('Scanning for known network...',0,0,0xffff); lcd.show()

    tries=3
    while tries > 0:
        nic.active(True)
        utime.sleep_ms(1500)
        for n in nic.scan():
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
        lcd.text('No known networks.',0,0,0xffff); lcd.show()
        utime.sleep_ms(1000)
        return False

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
    return True

def create_synchronised_time(lcd,key):
    if do_connect(lcd,key):
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

    else:
        # Wifi (and thus NTP) failed, so we fallback to manual
        # year, month, day, hours, minutes, seconds)
        datetime = [d for d in time.localtime()[0:6]]
        # Rollover limits
        min_dt = [2023,1,1,0,0,0]
        max_dt = [2300,12,31,59,59,59]
        selected_idx = 0
        max_idx=len(datetime)

        display_width = display.get_width()
        display_height = display.get_height()

        display.clear()
        display.text("Inc", 0, 0)
        display.text("Dec", 0, display_height - 9)
        display.text("Next", display_width - 30, display_height - 9)

        display.text("YYYY MM DD HH MM SS", 0, display_height // 2 - 20)

        changed=True

        while True:
            if rp2.bootsel_button():
                changed=True
                selected_idx = (selected_idx + 1) % (max_idx+1)
            if selected_idx < max_idx:
                if display.is_pressed(display.KEY0):
                    changed=True
                    datetime[selected_idx] += 1
                    if datetime[selected_idx] > max_dt[selected_idx]:
                        datetime[selected_idx] = min_dt[selected_idx]
                if display.is_pressed(display.KEY1):
                    changed=True
                    datetime[selected_idx] -= 1
                    if datetime[selected_idx] < min_dt[selected_idx]:
                        datetime[selected_idx] = max_dt[selected_idx]
            else:
                if display.is_pressed(display.KEY0):
                    break

            if changed:
                display.fill_rect(0, display_height // 2, display_width, 9, 0x0000)
                display.text(
                    " ".join("%s%02d" % (">" if idx == selected_idx else "", sep)
                             for idx, sep in enumerate(datetime)),
                    0, display_height // 2)
                if selected_idx < max_idx:
                    display.fill_rect(0, 0, 21, 9, 0x0000)
                    display.text("Inc", 0, 0)
                else:
                    display.fill_rect(0, 0, 21, 9, 0x0000)
                    display.fill_rect(0, 0, 14, 9, 0xffff)
                    display.text("OK", 0, 0, 0x0000)

                display.show()
                changed=False
            time.sleep_ms(300)

        delta = time.mktime(datetime + [0, 0]) - int(time.time())

        def synchronised_time():
            return int(time.time()) + delta

    return synchronised_time
