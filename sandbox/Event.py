from typing import List, Tuple
from datetime import datetime


class Event:
    def __init__(self, event_opt: List[str]) -> None:
        self.__event_opt_default = {
            "start": True,
            "end": True,
            "location": True,
            "description": True,
            "summary": True
        }
        self.event_opt = event_opt
        # self.event_normalize_opt = self.__get_normalize_event(event_opt)
#    'summary'= 'Google I/O 2015',
#   '?location'= '800 Howard St., San Francisco, CA 94103',
#     '?description'= 'A chance to hear more about Google\'s developer products.',
    # "?start=date:,datatime:,dateTime:"

    def __get_event_opt_key(self, key: str):
        return self.__event_opt_default.get(key, None)

    def __create_date(self, key, value):
        if key is not "dateTime" or key is "date":
            return value
        try:
            date = datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
            return date.isoformat()
        except ValueError as err:
            return False
