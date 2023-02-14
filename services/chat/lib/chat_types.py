
from typing import Optional, TypeVar
from dataclasses import dataclass


@dataclass
class Message:
    message_id: Optional[int]
    user_id: Optional[int]
    content: str
    date: str
    is_bot: bool


@dataclass
class Event:
    start: str
    end: str
    location: str
    summary: str
    # description: str


@dataclass
class ParamOption:
    field_name: str
    token: str

    def keys(self):
        return ["field_name", "token"]

    def __getitem__(self, key):
        return self.__getattribute__(key)


@dataclass
class ParamsLocations:
    token: str
    min: int
    max: int
