import LCD_1in44
import RPi.GPIO as GPIO
import locale
import logging
import random
import requests
import time
from PIL import Image, ImageDraw
from statistics import mean
from datetime import datetime, timedelta

logging.basicConfig(level="INFO")
log = logging.getLogger("main")

def days_to_mail_delivery():
    log.info("getting days until mail delivery")

    locale.setlocale (locale.LC_TIME, "sv_SE.UTF-8")
    next_mail_url = "https://portal.postnord.com/api/sendoutarrival/closest?postalCode=41872"
    response = requests.get(next_mail_url)

    if response.status_code >= 400:
        raise RuntimeError("unable to get page")

    data = response.json()
    delivery_str = data['delivery']
    delivery_time = datetime.strptime(delivery_str, "%d %B, %Y")
    delivery_date = delivery_time.date()

    today = datetime.today().date()

    # datetime.today
    date_diff = delivery_date - today
    return date_diff.days

def todays_electrical_prices():
    log.info("getting todays electricity prices")

    today = datetime.strftime(datetime.today(), "%Y-%m-%d")
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
        "accept": "application/json,text/html;q=0.99,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    spot_price_url = f"https://www.vattenfall.se/api/price/spot/pricearea/{today}/{today}/SN3"
    response = requests.get(spot_price_url, headers=headers)

    if response.status_code >= 400:
        raise RuntimeError("unable to get page")

    prices = [ val['Value'] for val in response.json() ]

    return { "min": min(prices), "mean": mean(prices), "max": max(prices) }

def retry(data_func):
    retry_time_seconds = 3

    # retry at most ten times
    for i in range(0, 10):
        try:
            res = data_func()
            if res != None:
                return res
        except Exception:
            log.exception("retrieval raised an error")
        
        log.info(f"waiting to retry for {retry_time_seconds} seconds")
        time.sleep(retry_time_seconds)
        retry_time_seconds = retry_time_seconds * 2
    
    raise RuntimeError("retry failed")

def draw_letter(draw, pos_x, pos_y, days):
    color = "GREEN"
    text = "IDAG"

    if days == 1:
        color = "YELLOW"
        text = "IMORGON"
    elif days == 2:
        color = "ORANGE"
        text = "OM 2 DAGAR"
    elif days > 2:
        color = "RED"
        text = "SENARE"

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

def main():
    LCD = LCD_1in44.LCD()

    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)
    LCD.LCD_Clear()

    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    days = retry(days_to_mail_delivery)
    prices = retry(todays_electrical_prices)

    next_update = tomorrow()
    log.info(f"next update time is {next_update}")

    while True:
        channel = GPIO.wait_for_edge(16, GPIO.FALLING, timeout=10000)
        if channel is not None:
            image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
            draw = ImageDraw.Draw(image)

            draw.rectangle([(0,0),(127,127)], fill="BLACK")
            draw_letter(draw, 15, 20, days)   
            draw_price(draw, 15, 70, prices)

            LCD.LCD_ShowImage(image,0,0)

            time.sleep(30)

            draw.rectangle([(0,0),(127,127)], fill="BLACK")
            LCD.LCD_ShowImage(image,0,0)

        elif (next_update - datetime.today()).total_seconds() < 0:
            days = retry(days_to_mail_delivery)
            prices = retry(todays_electrical_prices)

            next_update = tomorrow()

            log.info(f"next update time is {next_update}")

if __name__ == '__main__':
    while True:
        try:
            main()
        except RuntimeError:
            log.exception("something unexpected occurred")
