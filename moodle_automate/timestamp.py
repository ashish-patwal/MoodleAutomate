from datetime import datetime, date, timedelta
import math

def timestamp() -> 'timestamp':
    """returns timestamps for calender events . Not usable for now as api is returning blank responces."""
    today = date.today() 
    today = datetime(today.year, today.month, today.day, 0, 0, 0)
    nextday = today + timedelta(days=7)

    timestamp = datetime.timestamp(today)
    nexttimestamp = datetime.timestamp(nextday)

    return [math.trunc(timestamp), math.trunc(nexttimestamp)]
