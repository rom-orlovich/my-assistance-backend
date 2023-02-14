from datetime import datetime
from typing import List


class DateUtils:

    formats: List[str]

    def __init__(self) -> None:
        self.formats = ['%d/%m/%Y,%H:%M',
                        '%d-%m-%y,%H:%M', "%d-%m-%Y", "%H:%M"]

    def convert(self, value: str, format: str = None):
        formats = self.formats
        if format:
            formats = [format, *formats]
        for format in formats:
            try:
                return datetime.strptime(value, format)
            except ValueError as e:
                print(e)

    def get_date_and_time(self, value: str, format: str = None, delimiter=","):
        default_format = format or self.formats[0]
        try:
            date_time = datetime.fromisoformat(
                value)
        except:
            date_time = datetime.strptime(value, default_format)
        date_str = date_time.strftime(default_format)
        date, time = date_str.split(delimiter)
        return date, time
