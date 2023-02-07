
from my_types import Message
import datetime
from Bot import bot


class Chat:
    def __init__(self) -> None:
        self.messages = list()
        self.message_id = 0
        self.create_message(bot.get_bot_response(""))

    def create_message(self, message: Message):
        self.message_id += 1
        new_message = {"id": self.message_id,
                       "date": datetime.datetime.now().isoformat(), "is_bot": False, **message}
        self.messages.append(new_message)

    def manage_chat(self, message: Message):
        self.create_message(message)
        bot_response = bot.get_bot_response(message.content)
        self.create_message(bot_response)

        return self.message_id

    def get_messages(self):
        return self.messages


chat = Chat()
