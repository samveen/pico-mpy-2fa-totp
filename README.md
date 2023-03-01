# Raspberry Pi Pico/MicroPython 2FA TOTP Generator

Generates Time-based One-Time Password's (TOTP) using MicroPython, Raspberry Pi Pico and a 20x4 or 16x2 [Character LCD](https://shopee.ph/1602-16x2-Character-LCD-Module-Display-HD44780-with-I2C-i.18252381.242465767).

<img src="example.gif" />

## Features

- Complete [MicroPython implementation](totp) of the TOTP specification (and underlying HMAC-SHA1, Base32 dependencies).
- Countdown timer to present how long till the TOTP is about to expire.
- Use WiFi network and NTP to set the current UTC time - to correct the Raspberry Pi Pico's RTC

## Usage

- Connect the [Character LCD](https://shopee.ph/1602-16x2-Character-LCD-Module-Display-HD44780-with-I2C-i.18252381.242465767) to the Raspberry Pi Pico.
- Create a `codes.json` file (based on `codes.json.example`) which includes the desired TOTP keys.
- Flash the Raspberry Pi Pico with the latest [MicroPython with Pimoroni Libs](https://github.com/pimoroni/pimoroni-pico/releases/latest).
- Copy the codebase to the Raspberry Pi Pico.
- Configure WiFi network SSID and password on `synchronised_time.py`.
- Now you can cycle through your TOTP's using a button.

## Acknowledgements

Forked from [pico-2fa-totp](https://github.com/eddmann/pico-2fa-totp) created by [Edd Mann](https://github.com/eddmann). 

RPI PICO I2C LCD scripts from [RPI-PICO-I2C-LCD](https://github.com/T-622/RPI-PICO-I2C-LCD) created by [Tyler Peppy](https://github.com/T-622).