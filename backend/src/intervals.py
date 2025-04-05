from datetime import timedelta
from datetime import datetime

INTERVALS = [
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "4h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
]


# Function to convert an interval to a duration (in minutes)
def interval_to_duration(interval: str) -> timedelta:
    if interval == "ytd":
        return datetime.now() - datetime(
            year=datetime.now().year, month=1, day=1
        )
    elif interval.endswith("m"):  # minutes
        return timedelta(minutes=int(interval[:-1]))
    elif interval.endswith("h"):  # hours
        return timedelta(hours=int(interval[:-1]))
    elif interval.endswith("d"):  # days
        return timedelta(days=int(interval[:-1]))
    elif interval.endswith("wk"):  # weeks
        return timedelta(weeks=int(interval[:-2]))
    elif interval.endswith("mo"):  # months (approx 30 days)
        return timedelta(days=30 * int(interval[:-2]))
    elif interval.endswith("y"):
        return timedelta(days=365 * int(interval[:-1]))
    else:
        raise ValueError("Unknown interval format")


# Function to convert a duration (timedelta) to an interval string
def duration_to_interval(duration: timedelta) -> str:
    total_minutes = duration.total_seconds() / 60

    # Match the closest interval from INTERVALS
    if total_minutes <= 1 * 60:
        return "1m"
    elif total_minutes <= 2 * 60:
        return "2m"
    elif total_minutes <= 5 * 60:
        return "5m"
    elif total_minutes <= 15 * 60:
        return "15m"
    elif total_minutes <= 30 * 60:
        return "30m"
    elif total_minutes <= 60 * 60:
        return "60m"
    elif total_minutes <= 90 * 60:
        return "90m"
    elif total_minutes <= 1 * 60 * 60:
        return "1h"
    elif total_minutes <= 4 * 60 * 60:
        return "4h"
    elif total_minutes <= 24 * 60 * 60:
        return "1d"
    elif total_minutes <= 5 * 24 * 60 * 60:
        return "5d"
    elif total_minutes <= 7 * 24 * 60 * 60:
        return "1wk"
    elif total_minutes <= 30 * 24 * 60 * 60:
        return "1mo"
    else:
        return "3mo"
