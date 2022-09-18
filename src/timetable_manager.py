import re
from typing import Match, Pattern

def convert_hour_to_seconds(hour: str) -> str:
    '''Receive an hour in HH:MM format 
    and transforms it in seconds.
    The seconds count from 00:00 to 23:59'''
    hours: int = int(hour)

    MINUTES_IN_HOUR: int = 60
    SECONDS_IN_MINUTE: int = 60
    SECONDS_IN_HOUR: int = MINUTES_IN_HOUR * SECONDS_IN_MINUTE
    return str(hours * SECONDS_IN_HOUR)

def parse_timetable_from_timetables(timetables: str) -> list[str]:
    re_timetable: Pattern = re.compile(r'(\d{2} a \d{2})')
    return re_timetable.findall(timetables)

def get_start_and_end_time_from_timetable(timetable: str) -> dict[str, str] :
    re_timetable: Pattern = re.compile(r'(\d{2}) a (\d{2})')
    start_hour: str
    end_hour: str
    hours_found: Match | None = re_timetable .search(timetable) 
    
    if hours_found:
        start_hour, end_hour = (
                hours_found.groups()
        )

        time_dict: dict[str, str] = {
            'start_time': start_hour,
            'end_time': end_hour

        }
        return time_dict
    else:
        raise Exception('the argument is not a timetable')

def parse_days(days: str) -> list[str]:
    re_days: Pattern = re.compile(r'(\w{2})')
    days_found = re_days.findall(days)
    return days_found

    





