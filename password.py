import time
import rp2

def get(display):
    # year, month, day, hours, minutes, seconds)
    password=[0,0,0,0,0,0,0,0]
    # Rollover limits
    chars=b'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()+=/?[]{};:,.<>|~'
    clen=len(chars)
    selected_idx = 0
    max_idx=len(password)

    display_width = display.get_width()
    display_height = display.get_height()

    display.clear()
    display.text("Inc", 0, 0)
    display.text("Dec", 0, display_height - 9)
    display.text("Next", display_width - 30, display_height - 9)

    display.text(" C C C C C C C C", 14, display_height // 2 - 15)

    changed=True

    while True:
        if rp2.bootsel_button():
            changed=True
            selected_idx = (selected_idx + 1) % (max_idx+1)
        if selected_idx < max_idx:
            if display.is_pressed(display.KEY0):
                changed=True
                password[selected_idx] += 1
                if password[selected_idx] == clen:
                    password[selected_idx] = 0
            if display.is_pressed(display.KEY1):
                changed=True
                password[selected_idx] -= 1
                if password[selected_idx] < 0:
                    password[selected_idx] = clen-1
        else:
            if display.is_pressed(display.KEY0):
                break

        if changed:
            display.fill_rect(0, display_height // 2, display_width, 9, 0x0000)
            display.text(
                " ".join("%s%c" % (">" if idx == selected_idx else "", chars[sep])
                         for idx, sep in enumerate(password)),
                21, display_height // 2+5)
            if selected_idx < max_idx:
                display.fill_rect(0, 0, 21, 9, 0x0000)
                display.text("Inc", 0, 0)
            else:
                display.fill_rect(0, 0, 21, 9, 0x0000)
                display.fill_rect(0, 0, 14, 9, 0xffff)
                display.text("OK", 0, 0, 0x0000)

            display.show()
            changed=False
        time.sleep_ms(100)

    display.clear()
    return "".join(chr(chars[sep]) for idx, sep in enumerate(password))
