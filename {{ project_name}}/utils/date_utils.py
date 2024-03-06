from datetime import datetime, timezone
from typing import Optional, Union

from dateutil.parser import parse

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def parse_datetime(
    input_timestamp: Optional[Union[str, datetime]]
) -> Optional[datetime]:
    if input_timestamp is None:
        return None
    elif isinstance(input_timestamp, datetime):
        return input_timestamp
    else:
        return parse(input_timestamp)


def format_datetime_for_veson(input_timestamp: Union[str, datetime]) -> str:
    timestamp = parse_datetime(input_timestamp=input_timestamp)
    timestamp_string = timestamp.strftime("%Y-%m-%dT%H:%M:%S%z")
    timestamp_string = "{0}:{1}".format(timestamp_string[:-2], timestamp_string[-2:])
    return timestamp_string


def convert_hrs_to_ddhhmm(double_value):
    # Convert the double value to total seconds
    total_seconds = int(float(double_value) * 3600)

    # Calculate days, hours, and remaining seconds
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format the result
    result = f"{days:02d}:{hours:02d}:{minutes:02d}"
    return result


def convert_gmt_offset_to_minutes(
    input_timestamp: Union[str, datetime]
) -> Optional[str]:
    timestamp = parse_datetime(input_timestamp=input_timestamp)
    timestamp_string = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f %z")
    gmt_offset_string = timestamp_string[-5:]
    hours = (
        int(gmt_offset_string[1:3])
        if gmt_offset_string[0] in ["+", "-"]
        else int(gmt_offset_string[:2])
    )
    minutes = int(gmt_offset_string[-2:])
    total_minutes = hours * 60 + minutes
    if gmt_offset_string[0] == "-":
        total_minutes *= -1
    return str(total_minutes)


def extract_timezone(input_timestamp: Union[str, datetime]) -> Optional[str]:
    timestamp = parse_datetime(input_timestamp=input_timestamp)
    timestamp_string = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f %z")
    return timestamp_string[-5:]


def format_datetime_add_gmt_offset(
    input_datetime_string: str, gmt_offset: str
) -> Optional[str]:
    # Parse the input datetime string
    parsed_datetime = datetime.strptime(input_datetime_string, "%Y-%m-%dT%H:%M")
    # Convert the datetime to UTC and format it
    timestamp_string = parsed_datetime.replace(tzinfo=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    timestamp_string += gmt_offset
    timestamp_string = "{0}:{1}".format(timestamp_string[:-2], timestamp_string[-2:])
    return timestamp_string


def get_hour_difference(
    first_input_timestamp: datetime, second_input_timestamp: datetime
) -> Optional[float]:
    time_difference = first_input_timestamp - second_input_timestamp
    hours_difference = time_difference.total_seconds() / 3600

    if hours_difference is None:
        return 0
    else:
        return round(hours_difference, 2)
