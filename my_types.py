
from typing import Optional
from dataclasses import dataclass


@dataclass
class Message:
    message_id: Optional[int]
    user_id: Optional[int]
    content: str
    date: str
    is_bot: bool
