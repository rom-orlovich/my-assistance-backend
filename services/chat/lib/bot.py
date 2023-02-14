
from dataclasses import dataclass
from typing import Dict


from services.chat.lib.calender import Calendar


class Bot:
    calender: Calendar

    def __init__(self, bot_response: Dict[str, str]):
        self.bot_responses = bot_response
        self.calender = Calendar()

    def get_bot_response(self, message: str):
        calendar_response = self.calender.parse_message(message)

        if calendar_response:

            content = calendar_response
        else:

            content = self.bot_responses.get(message, "How can I help you?")
        return {"content": content, "is_bot": True}
