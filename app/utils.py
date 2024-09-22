from datetime import datetime
from dateutil import parser
import pytz

from flask import jsonify


def parse_datetime(datetime_str: str) -> datetime:
    """
    Parse a datetime string with timezone and return it in UTC.
    """
    # Parse the input string to a datetime object with timezone info
    local_datetime = parser.parse(datetime_str)

    # Convert to UTC and return the result
    utc_datetime = local_datetime.astimezone(pytz.UTC)

    return utc_datetime


def create_response(message, status_code, data=None, token=None):
    response = {
        "message": message,
    }

    if data is not None:
        response["data"] = data

    if token is not None:
        response["token"] = token

    return jsonify(response), status_code
