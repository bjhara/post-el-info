import locale
import logging
import requests

from datetime import datetime
from statistics import mean
from time import sleep
from typing import TypeVar, Callable, Any, Dict

T = TypeVar("T")


log = logging.getLogger("services")


def retry(data_func: Callable[[], T]) -> T:
    """Retry getting data from the supplied function using an exponential backoff."""
    retry_time_seconds = 3

    # retry at most ten times
    for i in range(0, 10):
        try:
            res = data_func()
            if res is not None:
                return res
        except Exception:
            log.exception("retrieval raised an error")
        
        log.info(f"waiting to retry for {retry_time_seconds} seconds")
        sleep(retry_time_seconds)
        retry_time_seconds = retry_time_seconds * 2
    
    raise RuntimeError("retry failed")

def days_to_mail_delivery() -> int:
    """Get the number of days until the next mail delivery for postal code 41872"""
    log.info("getting days until mail delivery")

    locale.setlocale (locale.LC_TIME, "sv_SE.UTF-8")
    next_mail_url = "https://portal.postnord.com/api/sendoutarrival/closest?postalCode=41872"
    response = requests.get(next_mail_url)

    if response.status_code >= 400:
        raise RuntimeError("unable to get page")

    data = response.json()

    date_diff = _days_from_today(data['delivery'])
    if date_diff < 0:
        log.info(f"next delivery was earlier, '{data['delivery']}', today is {datetime.today()}")
        date_diff = _days_from_today(data['upcoming'])

    return date_diff

def todays_electrical_prices() -> Dict[str, Any]:
    """Get todays electical prices for region SE3."""
    log.info("getting todays electricity prices")

    start_of_day = datetime.combine(datetime.today(), time.min)
    sod_ts = int(start_of_day.timestamp())
    end_of_day = datetime.combine(datetime.today(), time.max)
    eod_ts = int(end_of_day.timestamp())

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
        "accept": "application/json,text/html;q=0.99,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }

    spot_price_url = f"https://selfserviceapi.www.vattenfall.se/elements/nordpool/aggregatedspotprices?deliveryAreas=SE3&currency=SEK&deliveryStart={sod_ts}&deliveryEnd={eod_ts}&resolution=15mins&timezone=CET"
    response = requests.get(spot_price_url, headers=headers)

    if response.status_code >= 400:
        raise RuntimeError("unable to get page")

    json = response.json()
    prices = [val["measurement"]["value"] for val in json["prices"]]
    prices_per_hour = [max(prices[i : i + 4]) for i in range(0, len(prices), 4)]

    return {"min": min(prices_per_hour), "mean": mean(prices_per_hour), "max": max(prices_per_hour), "all": prices_per_hour}

def _days_from_today(time_string: str) -> int:
    parsed_time = datetime.strptime(time_string, "%d %B, %Y")
    the_date = parsed_time.date()
    today = datetime.today().date()

    return (the_date - today).days