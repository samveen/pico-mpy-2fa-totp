import machine

# function to save the RTC
def rtSaverCallback(t):
    from ustruct import pack
    r=machine.RTC()
    with open("hwclock.save","w") as fw: fw.write(pack("<8I",*(r.datetime())))

# Load the saved RTC time, and start the rtc saver save timer
def fakehwclock():
    from ustruct import unpack
    r=machine.RTC()
    # Restore RTC save
    try:
        with open("hwclock.save","rb") as fr: r.datetime(unpack("<8I",fr.read()))
    except OSError as e:
        r.datetime((2023, 1, 29, 6, 13, 55, 0, 0))
    except ValueError as e:
        r.datetime((2023, 2, 9, 4, 19, 8, 0, 0))

    # periodic firing of the function every 5000ms
    rtsaver = machine.Timer(mode=machine.Timer.PERIODIC, period=5000, callback=rtSaverCallback)


def board_init():
    # Turn on the LED
    machine.Pin("LED", machine.Pin.OUT).value(1)

    fakehwclock()
    r=machine.RTC()

board_init()
