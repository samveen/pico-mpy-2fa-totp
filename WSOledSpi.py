from machine import Pin,SPI
import framebuf
import time
import BasicFont

# Pin Definitions
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

display=None

class OLED_1inch3_SPI(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 64

        self.white =   0xffff
        self.black =   0x0000

        self.font=BasicFont.BasicFontCondensed

        # framebuf init
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)

        # SPI init
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,2000_000)
        self.spi = SPI(1,20000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)

        # display init
        self.init_display()

        # Clear the screen on init - needs frambuf init, spi init and display init
        self.clear()

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)

        self.write_cmd(0xAE)#turn off OLED display

        self.write_cmd(0x00)   # set lower column address
        self.write_cmd(0x10)   # set higher column address

        self.write_cmd(0xB0)   # set page address

        self.write_cmd(0xdc)   # set display start line
        self.write_cmd(0x00)   # (2nd param)

        self.write_cmd(0x81)   # contract control
        self.write_cmd(0x80)   # 128

        self.write_cmd(0x21)   # Set Memory addressing mode (0x20/0x21) #
        self.write_cmd(0xa0)   # set segment remap
        self.write_cmd(0xc0)   # Com scan direction
        self.write_cmd(0xa4)   # Disable Entire Display On (0xA4/0xA5)
        self.write_cmd(0xa6)   # normal / reverse

        self.write_cmd(0xa8)   # multiplex ratio ??
        self.write_cmd(0x3f)   # duty = 1/64 ??

        self.write_cmd(0xd3)   # set display offset
        self.write_cmd(0x60)

        self.write_cmd(0xd5)   # set osc division
        self.write_cmd(0x50)

        self.write_cmd(0xd9)   # set pre-charge period
        self.write_cmd(0x22)

        self.write_cmd(0xdb)   # set vcomh
        self.write_cmd(0x35)

        self.write_cmd(0xad)   # set charge pump enable
        self.write_cmd(0x8a)    #Set DC-DC enable (a=0:disable; a=1:enable)

        self.write_cmd(0XAF)   # turn on display

    def show(self):
        self.write_cmd(0xb0)
        for page in range(0,64):
            self.column = 63 - page
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0,16):
                self.write_data(self.buffer[page*16+num])

    def clear(self):
        self.fill(self.black)
        self.show()

    def text(self,s,x0,y0,col=0xffff):
        x=x0
        for i in range(len(s)):
            C = ord(s[i])
            if C < 32 or C > 127:
                C = 32
            cdata = self.font[C - 32]
            if x+len(cdata) > self.width:
                x=0
                y0=y0+9
            for j in range(len(cdata)):
                if 0 <= x and x < self.width:
                    vline_data = cdata[j]
                    y = y0
                    while vline_data:
                        if  vline_data & 1:
                            if  0 <= y and y < self.height:
                                self.pixel(x, y, col);
                        vline_data=vline_data>>1
                        y=y+1
                x=x+1
        return [x,y0+9]

def get():
    global display
    if display is None:
        display=OLED_1inch3_SPI()
    return display
