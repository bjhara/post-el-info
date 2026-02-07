import RPi.GPIO as GPIO # type: ignore
import logging
import random
import time

from PIL import Image, ImageDraw
from datetime import datetime, timedelta
from math import ceil
from names import todays_names
from services import retry, days_to_mail_delivery, todays_electrical_prices
from typing import Any, Dict, List, Optional
from WaveshareLcd import LCD, LCD_1IN44_Pins, LCD_1IN44_Config

LOW_PRICE = 50
HIGH_PRICE = 130
UPPER_DRAW_PRICE = 170

logging.basicConfig(level="INFO")
log = logging.getLogger("main")

def draw_letter(draw: ImageDraw.ImageDraw, pos_x: float, pos_y: float, days: int) -> None:
    color = "GREEN"
    text = "TODAY"

    if days == 1:
        color = "YELLOW"
        text = "TOMORROW"
    elif days == 2:
        color = "ORANGE"
        text = "IN 2 DAYS"
    elif days > 2:
        color = "RED"
        text = "LATER"

    WIDTH = 30
    HEIGHT = 20
    draw.line([(pos_x, pos_y), (pos_x + WIDTH, pos_y)], fill=color, width=2)
    draw.line([(pos_x + WIDTH, pos_y), (pos_x + WIDTH, pos_y + HEIGHT)], fill=color, width=2)
    draw.line([(pos_x, pos_y+HEIGHT), (pos_x + WIDTH, pos_y + HEIGHT)], fill=color, width=2)
    draw.line([(pos_x, pos_y), (pos_x, pos_y + HEIGHT)], fill=color, width=2)
    draw.line([(pos_x, pos_y), (pos_x + WIDTH, pos_y + HEIGHT)], fill=color, width=2)
    draw.line([(pos_x, pos_y + HEIGHT), (pos_x + WIDTH, pos_y)], fill=color, width=2)
    draw.text((pos_x + WIDTH + 7, pos_y + 5), text)

def color_for_price(price: float) -> str:
    color = "RED"
    if price < LOW_PRICE:
        color = "GREEN"
    elif price < HIGH_PRICE:
        color = "YELLOW"
    return color

def draw_price(draw: ImageDraw.ImageDraw, pos_x: float, pos_y: float, price: Dict[str, Any]) -> None:
    WIDTH = (128 - pos_x * 2) // 3
    HEIGHT = 20

    start_x = pos_x
    for name in [ "min", "mean", "max"]:
        color = color_for_price(price[name])

        draw.rectangle(((start_x, pos_y), (start_x + WIDTH, pos_y + HEIGHT)), fill=color)
        draw.text((start_x + 3, pos_y + 5), name.upper(), fill="BLACK")

        start_x = start_x + WIDTH

    draw_all_prices(draw, pos_x, pos_y + HEIGHT + 3, price["all"])

def draw_all_prices(draw: ImageDraw.ImageDraw, pos_x: float, pos_y: float, prices: List[float]) -> None:
    """Draw a small graph of all the given prices"""
    WIDTH = (128 - pos_x * 2) // len(prices)
    HEIGHT = 30

    start_x = pos_x
    for price in prices:
        color = color_for_price(price)
        price_height = max(min(ceil(HEIGHT * (price / UPPER_DRAW_PRICE)), HEIGHT), 1)
        draw.rectangle(((start_x, pos_y), (start_x + WIDTH, pos_y + price_height)), fill=color)
        start_x = start_x + WIDTH

def draw_names(draw: ImageDraw.ImageDraw, pos_x: float, pos_y: float, names: List[str]) -> None:
    all_names = ", ".join(names)
    draw.text((pos_x, pos_y), all_names.upper(), fill="WHITE")

def tomorrow() -> datetime:
    """Get a date representing sometime early tomorrow with a bit of randomness"""
    next_day = datetime.today() + timedelta(days = 1)
    minute = random.randrange(10, 60)
    second = random.randrange(0, 60)
    return next_day.replace(hour=0, minute=minute, second=second, microsecond=0)

def setup_hardware() -> LCD:
    """Initialise LCD and GPIO"""
    lcd = LCD(LCD_1IN44_Config, LCD_1IN44_Pins)
    
    lcd.backlight(False)
    lcd.sleep_in(True)

    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return lcd

def display_content(lcd: LCD, days: Optional[int], prices: Optional[Dict[str, Any]], names: List[str]) -> None:
    """Display content on screen for 30 seconds."""
    image = Image.new("RGB", (lcd.width, lcd.height), "WHITE")
    draw = ImageDraw.Draw(image)

    draw.rectangle(((0,0),(127,127)), fill="BLACK")
    if days is not None:
        draw_letter(draw, 15, 10, days)

    if prices is not None:
        draw_price(draw, 15, 40, prices)

    draw_names(draw, 15, 105, names)

    # wake it up and show the image
    lcd.sleep_in(False)
    lcd.display_image(image)
    lcd.backlight(True)

    time.sleep(30)

    # go back to sleep
    lcd.backlight(False)
    lcd.sleep_in(True)

def update_loop(lcd: LCD) -> None:
    days = retry(days_to_mail_delivery)
    prices = retry(todays_electrical_prices)
    names = todays_names()

    next_update = tomorrow()
    log.info(f"next update time is {next_update}")

    while True:
        # display information when button is pressed
        channel = GPIO.wait_for_edge(16, GPIO.FALLING, timeout=10000)
        if channel is not None:
            display_content(lcd, days, prices, names)

        elif (next_update - datetime.today()).total_seconds() < 0:
            days = retry(days_to_mail_delivery)
            prices = retry(todays_electrical_prices)
            names = todays_names()

            next_update = tomorrow()

            log.info(f"next update time is {next_update}")

def main() -> None:
    lcd = setup_hardware()

    while True:
        try:
            update_loop(lcd)
        except RuntimeError:
            log.exception("something unexpected occurred")

if __name__ == '__main__':
    main()
