import math
from datetime import datetime, date, timedelta


def timestamp() -> list[int]:
    """returns timestamps for calender events . Not usable for now as api is returning blank responces."""
    today = date.today()
    today = datetime(today.year, today.month, today.day, 0, 0, 0)
    nextday = today + timedelta(days=7)

    time_stamp = datetime.timestamp(today)
    next_time_stamp = datetime.timestamp(nextday)

    return [math.trunc(time_stamp), math.trunc(next_time_stamp)]
