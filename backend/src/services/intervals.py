import datetime as dt

TIMEZONE = dt.UTC
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
def interval_to_duration(interval: str) -> dt.timedelta:
    if interval == "ytd":
        return now() - dt.datetime(
            year=now().year,
            month=1,
            day=1,
            tzinfo=TIMEZONE,
        )
    if interval.endswith("m"):  # minutes
        return dt.timedelta(minutes=int(interval[:-1]))
    if interval.endswith("h"):  # hours
        return dt.timedelta(hours=int(interval[:-1]))
    if interval.endswith("d"):  # days
        return dt.timedelta(days=int(interval[:-1]))
    if interval.endswith("wk"):  # weeks
        return dt.timedelta(weeks=int(interval[:-2]))
    if interval.endswith("mo"):  # months (approx 30 days)
        return dt.timedelta(days=30 * int(interval[:-2]))
    if interval.endswith("y"):
        return dt.timedelta(days=365 * int(interval[:-1]))
    msg = "Unknown interval format"
    raise ValueError(msg)


# Function to convert a duration (dt.timedelta) to an interval string
def duration_to_interval(duration: dt.timedelta) -> str:
    total_minutes = duration.total_seconds() / 60

    # Match the closest interval from INTERVALS
    if total_minutes <= 1 * 60:
        return "1m"
    if total_minutes <= 2 * 60:
        return "2m"
    if total_minutes <= 5 * 60:
        return "5m"
    if total_minutes <= 15 * 60:
        return "15m"
    if total_minutes <= 30 * 60:
        return "30m"
    if total_minutes <= 60 * 60:
        return "60m"
    if total_minutes <= 90 * 60:
        return "90m"
    if total_minutes <= 1 * 60 * 60:
        return "1h"
    if total_minutes <= 4 * 60 * 60:
        return "4h"
    if total_minutes <= 24 * 60 * 60:
        return "1d"
    if total_minutes <= 5 * 24 * 60 * 60:
        return "5d"
    if total_minutes <= 7 * 24 * 60 * 60:
        return "1wk"
    if total_minutes <= 30 * 24 * 60 * 60:
        return "1mo"
    return "3mo"


def now() -> dt.datetime:
    return dt.datetime.now(TIMEZONE)
