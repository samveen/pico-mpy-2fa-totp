# Raspberry Pi Pico/MicroPython 2FA TOTP Generator

Generates Time-based One-Time Password's (TOTP) using MicroPython, Raspberry Pi Pico W and the [Waveshare Pico-Oled-1.3](https://www.waveshare.com/product/pico-oled-1.3.htm).

<img src="example.gif" />

## Features

- Complete [MicroPython implementation](totp) of the TOTP specification (and underlying HMAC-SHA1, Base32 dependencies).
- Countdown timer to present how long till the TOTP is about to expire.
- Use WiFi network and NTP to set the current UTC time - to correct the Raspberry Pi Pico's RTC


## Usage

- Connect the display to the Raspberry Pi Pico W.
- Create a `codes.json` file (based on `codes.json.example`) which includes the desired TOTP keys.
- Flash the Pico W with the latest [MicroPython](https://micropython.org/download/rp2-pico-w/).
- Configure WiFi network SSID and password on `synchronised_time.py`.
- Copy the codebase to the Raspberry Pi Pico W.
- Reset the Pico W
- Now you can cycle through your TOTP's using a button.


## Acknowledgements

Forked from [Kleo's](https://github.com/kleo) [fork](https://github.com/kleo/pico-2fa-totp) of the [pico-2fa-totp](https://github.com/eddmann/pico-2fa-totp) created by [Edd Mann](https://github.com/eddmann).

Pico-oled-1.3 driver by [Waveshare](https://www.waveshare.com/wiki/Pico-OLED-1.3#Examples) updated with [nicer fonts](https://github.com/markwinap/Pycom-SH1107-I2C/blob/master/lib/SH1107.py).
