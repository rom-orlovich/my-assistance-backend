
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
