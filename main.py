import LCD_1in44
import RPi.GPIO as GPIO
import logging
import random
import time
from PIL import Image, ImageDraw
from datetime import datetime, timedelta
from services import retry, days_to_mail_delivery, todays_electrical_prices

logging.basicConfig(level="INFO")
log = logging.getLogger("main")

def draw_letter(draw, pos_x, pos_y, days):
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

def draw_price(draw, pos_x, pos_y, price):
    WIDTH = (128 - pos_x * 2) // 3
    HEIGHT = 20

    start_x = pos_x
    for name in [ "min", "mean", "max"]:
        color = "RED"
        if price[name] < 50:
            color = "GREEN"
        elif price[name] < 150:
            color = "YELLOW"

        draw.rectangle([(start_x, pos_y), (start_x + WIDTH, pos_y + HEIGHT)], fill=color)
        draw.text((start_x + 3, pos_y + 5), name.upper(), fill="BLACK")

        start_x = start_x + WIDTH

def tomorrow():
    """Get a date representing sometime early tomorrow with a bit of randomness"""
    next_day = datetime.today() + timedelta(days = 1)
    minute = random.randrange(10, 60)
    second = random.randrange(0, 60)
    return next_day.replace(hour=0, minute=minute, second=second, microsecond=0)

def setup_hardware():
    """Initialise LCD and GPIO"""
    LCD = LCD_1in44.LCD()

    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)
    LCD.LCD_Clear()

    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return LCD

def display_content(LCD, days, prices):
    """Display content on screen for 30 seconds."""
    image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
    draw = ImageDraw.Draw(image)

    draw.rectangle([(0,0),(127,127)], fill="BLACK")
    draw_letter(draw, 15, 20, days)   
    draw_price(draw, 15, 70, prices)

    LCD.LCD_ShowImage(image,0,0)

    time.sleep(30)

    draw.rectangle([(0,0),(127,127)], fill="BLACK")
    LCD.LCD_ShowImage(image,0,0)

def update_loop(LCD):
    days = retry(days_to_mail_delivery)
    prices = retry(todays_electrical_prices)

    next_update = tomorrow()
    log.info(f"next update time is {next_update}")

    while True:
        # display information when button is pressed
        channel = GPIO.wait_for_edge(16, GPIO.FALLING, timeout=10000)
        if channel is not None:
            display_content(LCD, days, prices)

        elif (next_update - datetime.today()).total_seconds() < 0:
            days = retry(days_to_mail_delivery)
            prices = retry(todays_electrical_prices)

            next_update = tomorrow()

            log.info(f"next update time is {next_update}")

def main():
    LCD = setup_hardware()

    while True:
        try:
            update_loop(LCD)
        except RuntimeError:
            log.exception("something unexpected occurred")

if __name__ == '__main__':
    main()
