import time
import rp2

def get(display):
    # year, month, day, hours, minutes, seconds)
    # 8 2-digit numbers
    password=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # Rollover limits
    chars=b'!#$%&()*+,./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~'
    clen=len(chars)
    selected_idx = 0
    max_idx=len(password)

    display_width = display.get_width()
    display_height = display.get_height()

    display.clear()
    display.text("Inc", 0, 0)
    display.text("Dec", 0, display_height - 9)
    display.text("Next", display_width - 30, display_height - 9)


    changed=True

    while True:
        if rp2.bootsel_button():
            changed=True
            selected_idx = (selected_idx + 1) % (max_idx+1)
        if selected_idx < max_idx:
            if display.is_pressed(display.KEY0):
                changed=True
                password[selected_idx] += 1
                if selected_idx%2:
                    if (password[selected_idx-1]*10+password[selected_idx]) >= clen or (password[selected_idx-1]//10 < clen//10 and password[selected_idx]>9):
                        password[selected_idx] = 0
                else:
                    if (password[selected_idx]*10+password[selected_idx+1]) >= clen:
                        password[selected_idx] = 0
            if display.is_pressed(display.KEY1):
                changed=True
                password[selected_idx] -= 1
                if selected_idx%2:
                    if password[selected_idx] < 0:
                        if password[selected_idx-1]//10 < clen//10:
                            password[selected_idx] = 9
                        else:
                            password[selected_idx] = (clen%10)-1
                else:
                    if password[selected_idx] < 0:
                        if password[selected_idx+1] >= clen%10:
                            password[selected_idx] = (clen//10)-1
                        else:
                            password[selected_idx] = (clen//10)
        else:
            if display.is_pressed(display.KEY0):
                break

        if changed:
            # Clear from (0,display_height//2 - 20),till (display_width, display_height // 2 + 10 + 7)
            display.fill_rect(0, display_height // 2 -20, display_width, 37, 0x0000)
            display.text(
                " ".join("%c" % chars[j] for j in [i[0]*10+i[1] for i in [password[k:k+2] for k in range(0,len(password),2)]]),
                14, display_height // 2 - 20)
            display.text(
                "".join("%02i" % (i[0]*10+i[1]) for i in [password[k:k+2] for k in range(0,len(password),2)]),
                (display_width-16*7)//2, display_height // 2)

            if selected_idx < max_idx:
                display.fill_rect(0, 0, 21, 9, 0x0000)
                display.text("Inc", 0, 0)
                display.text("^", (display_width-16*7)//2 - 1 + selected_idx*7, display_height // 2 + 10)
                display.rect((display_width-16*7)//2 - 1 + ((selected_idx>>1)<<1)*7, display_height//2 - 2 ,15,1,0xffff)

            else:
                display.fill_rect(0, 0, 21, 9, 0x0000)
                display.fill_rect(0, 0, 14, 9, 0xffff)
                display.text("OK", 0, 0, 0x0000)

            display.show()
            changed=False
        time.sleep_ms(100)

    display.clear()
    return "".join(chr(chars[j]) for j in [i[0]*10+i[1] for i in [password[k:k+2] for k in range(0,len(password),2)]])
