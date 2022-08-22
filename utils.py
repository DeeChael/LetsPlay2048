import datetime
import re


def parse_time(time_str: str) -> datetime.timedelta:
    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    for item in re.compile("\\d+(y|mo|wk|d|h|min|s)").match(time_str).groups():
        if item.endswith("y"):
            days += int(item[0:len(item) - 1]) * 365
        elif item.endswith("mo"):
            days += int(item[0:len(item) - 2]) * 30
        elif item.endswith("wk"):
            weeks += int(item[0:len(item) - 2])
        elif item.endswith("d"):
            days += int(item[0:len(item) - 1])
        elif item.endswith("h"):
            hours += int(item[0:len(item) - 1])
        elif item.endswith("min"):
            minutes += int(item[0:len(item) - 3])
        elif item.endswith("s"):
            seconds += int(item[0:len(item) - 1])
    return datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
