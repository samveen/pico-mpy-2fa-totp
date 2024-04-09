import machine
import ustruct as struct

# Common RTC
r=None
rtsaver=None

# function to save the RTC
def rtSaverCallback(t):
    global r
    with open("hwclock.save","w") as fw: fw.write(struct.pack("<8I",*(r.datetime())))

# Load the saved RTC time, and start the rtc saver save timer
def fakehwclock():
    global r
    global rtsaver
    # Restore RTC save
    try:
        with open("hwclock.save","rb") as fr: r.datetime(struct.unpack("<8I",fr.read()))
    except OSError as e:
        r.datetime((2024, 4, 9, 6, 04, 55, 0, 0))
    except ValueError as e:
        r.datetime((2024, 4, 9, 6, 04, 55, 0, 0))

    # periodic firing of the function every 5000ms
    if rtsaver == None:
        rtsaver = machine.Timer(mode=machine.Timer.PERIODIC, period=5000, callback=rtSaverCallback)

def board_init():
    global r
    # Turn on the LED
    machine.Pin("LED", machine.Pin.OUT).value(1)
    # Init the common RTC
    r=machine.RTC()

    fakehwclock()

board_init()
