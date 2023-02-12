
from dataclasses import dataclass
from typing import Dict
import datetime
from Calendar import END_POINTS, Calendar
calendar = Calendar()


class Bot:
    def __init__(self, bot_response: Dict[str, str]):
        self.bot_responses = bot_response

    def get_bot_response(self, message: str):
        calendar_response = calendar.parse_message(message)
        if calendar_response:
            content = calendar_response
        else:
            content = self.bot_responses.get(message, "How can I help you?")
        return {"content": content, "is_bot": True}


bot = Bot({"hello": "Hey!",
           "how are you?": 'Fine!', "what are you doing?": "Nothing.", "what is the time?": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})
