from machine import Pin
from time import sleep_ms,time
import json
from totp import totp
import WSOledSpi

from synchronised_time import create_synchronised_time, do_connect

lcd = WSOledSpi.get()

button = Pin(15,Pin.IN,Pin.PULL_UP)
keyNext= Pin(17,Pin.IN,Pin.PULL_UP)
codes = json.loads(open("codes.json", "r").read())
selected_idx = 0
code = None

do_connect(lcd)

# Do all required init i.e. manual time setting vs ntp
synchronised_time = create_synchronised_time(lcd)

# Begin,End markers for timer bar
lcd.fill_rect(0,61,4,2,lcd.white)
lcd.fill_rect(124,61,4,2,lcd.white)
# Size of text area to be wiped first time: full screen minus timer bar height of 4
# (Set this correctly and let the text clearing code handle this instead
# of lcd.clear() or lcd.fill().)
loc=(lcd.width,lcd.height-4)

while True:
    # Is a button pressed
    if button.value() == 0:
        selected_idx = (selected_idx + 1) % len(codes)

    # Did the selection change from last time
    if code != codes[selected_idx]:
        code = codes[selected_idx]
        (password, expiry) = totp(synchronised_time(),
                                  code['key'],
                                  step_secs=code['step'],
                                  digits=code['digits'])

    # is it time to recalculate things yet?
    s=time()%30
    if s == 0:
        (password, expiry) = totp(synchronised_time(),
                                  code['key'],
                                  step_secs=code['step'],
                                  digits=code['digits'])

    # Wipe previous text (first run wipes full screen except timer bar)
    lcd.fill_rect(0,0,128,loc[1],0x0000)
    loc=lcd.text(code['name'],0,0,0xffff)
    loc=lcd.text(password,0,loc[1],0xffff)

    # Time left bar
    if s == 0:
        lcd.fill_rect(4,60,120,4,0x0000)
    lcd.fill_rect(4,60,(s+1)<<2,4,0xffff)
    lcd.show()
    sleep_ms(500)

