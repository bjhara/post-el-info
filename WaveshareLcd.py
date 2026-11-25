"""Library for Waveshare 1.44inch LCD HAT

Uses the RPi.GPIO compatible API provided by python3-rpi-lgpio (which talks
to /dev/gpiochipN through lgpio) and the kernel SPI driver via /dev/spidevB.D.
SPI must be enabled (dtparam=spi=on) and the user needs to be a member of the
gpio and spi groups.
"""
from dataclasses import dataclass
from enum import Enum
from PIL import Image
from typing import Sequence, Union

import numpy as np
import RPi.GPIO as GPIO # type: ignore
import spidev # type: ignore
import time


class ScanType(Enum):
    """Enum for the scan direction of the LCD"""
    L2R_U2D = 1
    L2R_D2U = 2
    R2L_U2D = 3
    R2L_D2U = 4
    U2D_L2R = 5
    U2D_R2L = 6
    D2U_L2R = 7
    D2U_R2L = 8


@dataclass(frozen=True)
class Config:
    """Basic configuration settings for the LCD"""
    width: int
    height: int
    x: int
    y: int
    rgb: bool
    scan_dir: ScanType


@dataclass(frozen=True)
class PinConfig:
    """Hardware interface configuration for the LCD

    Pin numbers use BCM numbering. Chip select is not listed since it is
    driven by the kernel SPI driver (CE0 for device 0); the GPIO is owned by
    that driver and can not be claimed through lgpio.
    """
    rst: int
    dc: int
    bl: int
    spi_bus: int
    spi_device: int
    spi_speed_hz: int = 9000000


LCD_1IN44_Config = Config(128, 128, 2, 1, True, ScanType.U2D_R2L)
LCD_1IN8_Config = Config(160, 128, 1, 2, False, ScanType.U2D_R2L)

# SPI bus 0, device 0 (/dev/spidev0.0, chip select on CE0/GPIO 8)
LCD_1IN44_Pins = PinConfig(rst=27, dc=25, bl=24, spi_bus=0, spi_device=0)
LCD_1IN8_Pins = PinConfig(rst=27, dc=25, bl=24, spi_bus=0, spi_device=0)

Bytes = Union[bytes, bytearray, Sequence[int]]


class LCD:
    """Class for using a Waveshare LCD HAT for Raspberry Pi Zero"""
    def __init__(self, config: Config, pins: PinConfig):
        self.__config = config
        self.__pins = pins
        self.__width = config.width
        self.__height = config.height
        self.__x_adjust = config.x
        self.__y_adjust = config.y
        self.__spi = spidev.SpiDev()
        self.__closed = False

        try:
            self.__init_lcd()
        except BaseException:
            self.__release()
            raise

    def close(self) -> None:
        """Turn off the display and release the SPI device and GPIO lines"""
        if self.__closed:
            return
        try:
            self.backlight(False)
            self.sleep_in(True)
        finally:
            self.__release()

    def __release(self) -> None:
        self.__closed = True
        self.__spi.close()
        if GPIO.getmode() is not None:
            GPIO.cleanup([self.__pins.rst, self.__pins.dc, self.__pins.bl])

    def __enter__(self) -> "LCD":
        return self

    def __exit__(self, *_) -> None:
        self.close()

    def __init_lcd(self) -> None:
        self.__init_gpio()

        self.__reset()
        self.__init_reg()

        self.__set_memory_data_access_control(self.__config.scan_dir)

        self.sleep_in(False)

        # turn on the display
        self.__write_reg(0x29)

        self.backlight(True)

    def __init_gpio(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__pins.rst, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.__pins.dc, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.__pins.bl, GPIO.OUT, initial=GPIO.LOW)

        self.__spi.open(self.__pins.spi_bus, self.__pins.spi_device)
        self.__spi.max_speed_hz = self.__pins.spi_speed_hz
        self.__spi.mode = 0b00

    def __init_reg(self) -> None:
        # ST7735R frame rate
        self.__write_reg(0xB1)
        self.__write_data([0x01, 0x2C, 0x2D])

        self.__write_reg(0xB2)
        self.__write_data([0x01, 0x2C, 0x2D])

        self.__write_reg(0xB3)
        self.__write_data([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D])

        # ST7735R display inversion control
        self.__write_reg(0xB4)
        self.__write_data([0x07])

        # ST7735R power sequence
        self.__write_reg(0xC0)
        self.__write_data([0xA2, 0x02, 0x84])

        self.__write_reg(0xC1)
        self.__write_data([0xC5])

        self.__write_reg(0xC2)
        self.__write_data([0x0A, 0x00])

        self.__write_reg(0xC3)
        self.__write_data([0x8A, 0x2A])

        self.__write_reg(0xC4)
        self.__write_data([0x8A, 0xEE])

        self.__write_reg(0xC5)  # VCOM
        self.__write_data([0x0E])

        # ST7735R gamma adjustment +
        self.__write_reg(0xE0)
        self.__write_data(
            [
                0x0F,
                0x1A,
                0x0F,
                0x18,
                0x2F,
                0x28,
                0x20,
                0x22,
                0x1F,
                0x1B,
                0x23,
                0x37,
                0x00,
                0x07,
                0x02,
                0x10,
            ]
        )

        # ST7735R gamma adjustment -
        self.__write_reg(0xE1)
        self.__write_data(
            [
                0x0F,
                0x1B,
                0x0F,
                0x17,
                0x33,
                0x2C,
                0x29,
                0x2E,
                0x30,
                0x30,
                0x39,
                0x3F,
                0x00,
                0x07,
                0x03,
                0x10,
            ]
        )

        # 65k color mode
        self.__write_reg(0x3A)
        self.__write_data([0x05])

    def __reset(self) -> None:
        """Perform hardware reset"""
        GPIO.output(self.__pins.rst, GPIO.HIGH)
        self.__delay_ms(100)
        GPIO.output(self.__pins.rst, GPIO.LOW)
        self.__delay_ms(100)
        GPIO.output(self.__pins.rst, GPIO.HIGH)
        self.__delay_ms(100)

    def __write_reg(self, reg: int) -> None:
        """Set write register"""
        GPIO.output(self.__pins.dc, GPIO.LOW)
        self.__spi.writebytes([reg])

    def __write_data(self, data: Bytes) -> None:
        """Write data to register (writebytes2 splits large buffers itself)"""
        GPIO.output(self.__pins.dc, GPIO.HIGH)
        self.__spi.writebytes2(data)

    def __delay_ms(self, ms: int) -> None:
        time.sleep(ms / 1000)

    def __set_memory_data_access_control(self, scan_dir: ScanType) -> None:
        """Set the displays scan and color transfer modes"""
        reg_data_map = {
            ScanType.L2R_U2D: 0x00,
            ScanType.L2R_D2U: 0x80,
            ScanType.R2L_U2D: 0x40,
            ScanType.R2L_D2U: 0x40 | 0x80,
            ScanType.U2D_L2R: 0x20,
            ScanType.U2D_R2L: 0x20 | 0x40,
            ScanType.D2U_L2R: 0x20 | 0x80,
            ScanType.D2U_R2L: 0x20 | 0x40 | 0x80,
        }

        if scan_dir in [
            ScanType.L2R_U2D,
            ScanType.L2R_D2U,
            ScanType.R2L_U2D,
            ScanType.R2L_D2U,
        ]:
            self.__width = self.__config.height
            self.__height = self.__config.width
        else:
            self.__width = self.__config.width
            self.__height = self.__config.height

        memory_access_reg_data = reg_data_map[scan_dir]

        if (memory_access_reg_data & 0x10) != 1:
            self.__x_adjust = self.__config.y
            self.__y_adjust = self.__config.x
        else:
            self.__x_adjust = self.__config.x
            self.__y_adjust = self.__config.y

        self.__write_reg(0x36)  # MX, MY, RGB mode
        if self.__config.rgb:
            self.__write_data([memory_access_reg_data | 0x08])
        else:
            self.__write_data([memory_access_reg_data & 0xF7])

    def __set_window(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        """Set the start position and size of the display area"""
        # set x coordinates
        self.__write_reg(0x2A)
        self.__write_data(
            [
                0x00,
                (start_x & 0xFF) + self.__x_adjust,
                0x00,
                ((end_x - 1) & 0xFF) + self.__x_adjust,
            ]
        )

        # set y coordinates
        self.__write_reg(0x2B)
        self.__write_data(
            [
                0x00,
                (start_y & 0xFF) + self.__y_adjust,
                0x00,
                ((end_y - 1) & 0xFF) + self.__y_adjust,
            ]
        )

        self.__write_reg(0x2C)

    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height

    def sleep_in(self, enable) -> None:
        """Enter or exit low power consumption mode, sleep in"""
        if enable:
            self.__write_reg(0x10)
        else:
            self.__write_reg(0x11)
            self.__delay_ms(120)

    def clear(self) -> None:
        """Clear the screen by setting it to all white"""
        buffer = b"\xff" * (self.__width * self.__height * 2)
        self.__set_window(0, 0, self.__width, self.__height)
        self.__write_data(buffer)

    def backlight(self, on: bool) -> None:
        """Turn the backlight on or off"""
        if on:
            GPIO.output(self.__pins.bl, GPIO.HIGH)
        else:
            GPIO.output(self.__pins.bl, GPIO.LOW)

    def display_image(self, image: Image.Image) -> None:
        """Display an image on the LCD"""
        if image is None:
            raise ValueError("an image must be suplied")

        if image.width != self.__width or image.height != self.__height:
            raise ValueError(
                f"image must have the same dimensions as the display ({self.__width}x{self.__height})"
            )

        # convert to RGB565, big endian
        img = np.asarray(image.convert("RGB"), dtype=np.uint8)
        pix = np.empty((self.__height, self.__width, 2), dtype=np.uint8)
        pix[..., 0] = (img[..., 0] & 0xF8) | (img[..., 1] >> 5)
        pix[..., 1] = ((img[..., 1] << 3) & 0xE0) | (img[..., 2] >> 3)

        self.__set_window(0, 0, self.__width, self.__height)
        self.__write_data(pix.tobytes())


if __name__ == "__main__":
    from PIL import Image, ImageDraw

    with LCD(LCD_1IN44_Config, LCD_1IN44_Pins) as lcd:
        lcd.clear()

        image = Image.new("RGB", (lcd.width, lcd.height), "WHITE")
        draw = ImageDraw.Draw(image)

        color = [ "Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Violet" ]
        for i in range(7):
            p: float = i * 9.0
            draw.rectangle(((p, p),(127-p,127-p)), fill=color[i])

        lcd.display_image(image)
        time.sleep(10)
