from datetime import datetime
from typing import List


class DateUtils:

    formats: List[str]

    def __init__(self) -> None:
        self.formats = ['%d/%m/%Y,%H:%M', '%d-%m-%y,%H:%M', "%d-%m-%Y"]

    def convert(self, value: str, format: str = None):
        formats = self.formats
        if format:
            formats = [format, *formats]
        for format in formats:
            try:
                print(datetime.strptime(value, format))
                return datetime.strptime(value, format)
            except ValueError as e:
                print(e)
