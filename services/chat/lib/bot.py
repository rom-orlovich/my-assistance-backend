from dataclasses import dataclass
from typing import Dict


from services.chat.lib.calender import Calendar


class Bot:
    """
    Represents the bot entity.
    The bot parses the user messages and responds accordingly.
    """
    calender: Calendar

    def __init__(self, bot_response: Dict[str, str]):
        self.bot_responses = bot_response
        self.calender = Calendar()

    def get_bot_response(self, message: str):
        """ 
         Parse the user message and return the bot response.

        Args:
            message (str): The Message of the user.

        Returns:
            _type_: The bot response.
        """
        calendar_response = self.calender.parse_message(message)
        if calendar_response:
            content = calendar_response
        else:
            content = self.bot_responses.get(message, "How can I help you?")
        return {"content": content, "is_bot": True}
