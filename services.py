import locale
import logging
import requests
import time
from statistics import mean
from datetime import datetime

log = logging.getLogger("services")

def retry(data_func):
    """Retry getting data from the supplied function using an exponential backoff."""
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

def days_to_mail_delivery():
    """Get the number of days until the next mail delivery for postal code 41872"""
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
    """Get todays electical prices for region SE3."""
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

