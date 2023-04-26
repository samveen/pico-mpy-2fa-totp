# Raspberry Pi Pico/MicroPython 2FA TOTP Generator

Generates Time-based One-Time Password's (TOTP) using MicroPython, Raspberry Pi Pico W and the [Waveshare Pico-Oled-1.3](https://www.waveshare.com/product/pico-oled-1.3.htm).

<img src="example.gif" />

## Features

- Complete [MicroPython implementation](totp) of the TOTP specification (and underlying HMAC-SHA1, Base32 dependencies).
- Countdown timer to present how long till the TOTP is about to expire.
- Encrypt OTP code data with user password.
- Use WiFi network and NTP to set the current UTC time - to correct the Raspberry Pi Pico W's RTC.
- Reinvent old functionality for datetime input 3 buttons instead of 4, as fallback if no WiFi available. (Note 1 below)
- Encrypt Wifi data with user password too


## Usage

- Connect the display to the Raspberry Pi Pico W.
- Create a `codes.json` file (based on `codes.json.example`) which includes the desired TOTP keys.
- Create a `WifiSecrets.json` file (based on `WifiSecrets.json.example`) which includes the common wifi SSIDs + passphrases available.
- Flash the Pico W with the latest [MicroPython](https://micropython.org/download/rp2-pico-w/).
- Copy the codebase except `main.py` to the Raspberry Pi Pico W.
- Open an interactive session on the Pico and encrypt the `codes.json` and `WifiSecrets.json` as below:
```
>>> import cryptor
>>> cryptor.encrypt('codes.json','mypasswd')
>>> cryptor.encrypt('WifiSecrets.json','mypasswd')
```
- Remove the unencrypted `WifiSecrets.json` and `codes.json` from the Pico W storage
- Copy main.py to the Pico
- Reset the Pico W
- Enter your password at the initial password prompt.
- Fix datetime at prompt if Wifi doesn't work.
- Now you can cycle through your TOTP's using Key0 of the Pico-Oled-1.3.
- Key1 of the Pico-Oled-1.3 toggles the display ON/OFF.

# Updating secrets

- Connect to the REPL
- Press CTRL-C to stop the code and bring up the prompt
- Run the following code to dump the secrets files to console as plain text:
```
>>> import cryptor
>>> print(cryptor.decrypt('codes.json.encoded','mypasswd').decode())
>>> print(cryptor.decrypt('WifiSecrets.json.encoded','mypasswd').decode())
```
- Copy the outputs into `codes.json` and `WifiSecrets.json` on your workstation, and update with new secrets as required.
- Push the updated `codes.json` and `WifiSecrets.json` to the Pico W.
- Encrypt `codes.json` and `WifiSecrets.json` and overwrite previous encoded files as below:
```
>>> import cryptor
>>> cryptor.encrypt('codes.json','mypasswd')
>>> cryptor.encrypt('WifiSecrets.json','mypasswd')
```
- Remove the unencrypted `WifiSecrets.json` and `codes.json` from the Pico W storage.

Notes:
1. The Bootsel button is used for user input as the pico-oled-1.3 only has 2 buttons

## Acknowledgements

Forked from [Kleo's](https://github.com/kleo) [fork](https://github.com/kleo/pico-2fa-totp) of the [pico-2fa-totp](https://github.com/eddmann/pico-2fa-totp) created by [Edd Mann](https://github.com/eddmann).

Pico-oled-1.3 driver by [Waveshare](https://www.waveshare.com/wiki/Pico-OLED-1.3#Examples) updated with [nicer fonts](https://github.com/markwinap/Pycom-SH1107-I2C/blob/master/lib/SH1107.py).
