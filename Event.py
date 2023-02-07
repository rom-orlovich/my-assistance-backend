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
        self.event_normalize_opt = self.__get_normalize_event(event_opt)
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

    # def __get_normalize_event(self, event_opt: List[str]):
        normalize_event = {}
        for event in self.event_opt:
            event_split = event.split("=")
            if len(event_split) == 0:
                continue
            elif self.__get_event_opt_key(event_split[0]) is None:
                continue
            else:
                prop_values_opt_split = event_split[1].split(",")
                if len(prop_values_opt_split) == 1:
                    normalize_event[event_split[0]] = event_split[1]
                else:
                    sub_values = {}
                    for prop_values_opt in prop_values_opt_split:
                        sub_values_opt_split = prop_values_opt.split("-")
                        if len(sub_values_opt_split) == 0:
                            continue
                        else:
                            value = self.__create_date(sub_values_opt_split[1])
                            if value is False:
                                return
                            else:
                                sub_values[sub_values_opt_split[0]
                                           ] = sub_values_opt_split[1]
                    normalize_event[event_split[0]] = sub_values
        return normalize_event


# \calendar\events\create?start=dateTime-07/02/2023 16:00:00?end=dateTime-07/02/2023 20:00:00?summary=Google I/O 2015?location=800 Howard St., San Francisco, CA 94103?description=A chance to hear more about Google\'s developer products
