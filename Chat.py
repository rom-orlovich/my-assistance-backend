
from Bot import Bot
from my_types import Message
import datetime


class Chat:
    def __init__(self) -> None:
        self.messages = list()
        self.message_id = 0
        self.bot = Bot({"hello": "Hey!",
                        "how are you?": 'Fine!', "what are you doing?": "Nothing.", "what is the time?": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})
        self.create_message(self.bot.get_bot_response(""))

    def create_message(self, message: Message):
        self.message_id += 1
        new_message = {"message_id": self.message_id,
                       "date": datetime.datetime.now().isoformat(), "is_bot": False, **message}
        print(new_message)
        self.messages.append(new_message)

    def manage_chat(self, message: Message):
        self.create_message(message)
        bot_response = self.bot.get_bot_response(message.get("content"))
        self.create_message(bot_response)

        return self.message_id

    def get_messages(self):
        return self.messages


chat = Chat()
