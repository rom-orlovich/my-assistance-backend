from dataclasses import dataclass
from typing import Dict
import datetime


class Bot:
    def __init__(self, bot_response: Dict[str, str]):
        self.bot_responses = bot_response

    def get_bot_response(self, message: str):

        return {"content": self.bot_responses.get(message, "How can I help you?"), "is_bot": True}


bot = Bot({"hello": "Hey!",
           "how are you?": 'Fine!', "what are you doing?": "Nothing.", "what is the time?": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})
