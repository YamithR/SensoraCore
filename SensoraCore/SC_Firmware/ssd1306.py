"""
MicroPython SSD1306 OLED driver (I2C, SPI)

This is a lightweight driver compatible with MicroPython's framebuffer API.
It is safe to include in device projects that require an SSD1306 128x64 OLED.

Credits: based on the MicroPython community driver (MIT-compatible).
"""
from micropython import const
import framebuf

# registers
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA1)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC8)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)


class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)

    # framebuffer proxy methods
    def fill(self, color):
        self.framebuf.fill(color)

    def pixel(self, x, y, color):
        self.framebuf.pixel(x, y, color)

    def hline(self, x, y, w, color):
        self.framebuf.hline(x, y, w, color)

    def vline(self, x, y, h, color):
        self.framebuf.vline(x, y, h, color)

    def line(self, x1, y1, x2, y2, color):
        self.framebuf.line(x1, y1, x2, y2, color)

    def text(self, string, x, y, color=1):
        self.framebuf.text(string, x, y, color)

    def fill_rect(self, x, y, w, h, color):
        self.framebuf.fill_rect(x, y, w, h, color)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        super().__init__(width, height, external_vcc)
        self.i2c = i2c
        self.addr = addr
        # control byte
        self._write_cmd = lambda buf: self.i2c.writeto(self.addr, bytearray([0x00]) + bytearray([buf]))
        self.init_display()

    def init_display(self):
        # Initialization sequence adapted for common SSD1306 128x64
        for cmd in (
            SET_DISP,             # display off
            SET_DISP_CLK_DIV, 0x80,
            SET_MUX_RATIO, self.height - 1,
            SET_DISP_OFFSET, 0x00,
            SET_DISP_START_LINE | 0x00,
            SET_CHARGE_PUMP, 0x14 if not self.external_vcc else 0x10,
            SET_MEM_ADDR, 0x00,
            SET_SEG_REMAP,
            SET_COM_OUT_DIR,
            SET_COM_PIN_CFG, 0x12 if self.height == 64 else 0x02,
            SET_CONTRAST, 0xCF if not self.external_vcc else 0x9F,
            SET_PRECHARGE, 0xF1 if not self.external_vcc else 0x22,
            SET_VCOM_DESEL, 0x30,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_DISP | 0x01,  # display on
        ):
            # write command bytes
            try:
                if isinstance(cmd, int):
                    self.i2c.writeto(self.addr, bytes([0x00, cmd]))
                else:
                    # shouldn't happen; safe guard
                    pass
            except Exception:
                pass

    def poweroff(self):
        self.i2c.writeto(self.addr, bytes([0x00, SET_DISP]))

    def poweron(self):
        self.i2c.writeto(self.addr, bytes([0x00, SET_DISP | 0x01]))

    def contrast(self, contrast):
        self.i2c.writeto(self.addr, bytes([0x00, SET_CONTRAST, contrast]))

    def show(self):
        # set column/page addresses then send buffer
        # column address
        self.i2c.writeto(self.addr, bytes([0x00, SET_COL_ADDR, 0, self.width - 1]))
        # page address
        self.i2c.writeto(self.addr, bytes([0x00, SET_PAGE_ADDR, 0, self.pages - 1]))

        # send buffer in chunks to avoid I2C limits
        chunk = 32
        for i in range(0, len(self.buffer), chunk):
            block = self.buffer[i:i+chunk]
            # prefix with 0x40 data control byte
            self.i2c.writeto(self.addr, bytes([0x40]) + block)


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        super().__init__(width, height, external_vcc)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        # optional hardware reset
        try:
            self.res.on()
        except Exception:
            pass

    def write_cmd(self, cmd):
        self.dc.off()
        self.cs.off()
        self.spi.write(bytes([cmd]))
        self.cs.on()

    def show(self):
        # bulk transfer via SPI
        self.dc.on()
        self.cs.off()
        self.spi.write(self.buffer)
        self.cs.on()
