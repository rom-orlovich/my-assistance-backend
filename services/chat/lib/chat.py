from services.chat.lib.bot import Bot
from services.chat.lib.chat_types import Message
import datetime


class Chat:
    """ 
    Manages the chat between the bot and the users.
    """

    def __init__(self) -> None:
        self.messages = list()
        self.message_id = 0
        self.bot = Bot({"hello": "Hey!",
                        "how are you?": 'Fine!',
                        "what are you doing?": "Nothing.",
                        "what is the time?": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})
        self.create_message(self.bot.get_bot_response(""))

    def create_message(self, message: Message) -> None:
        """ 
        Create a new message dict that will append to the message list.
        After new message was created the message_id will increase by one.
        Args:
            message (Message): Message class 
        """
        self.message_id += 1
        new_message = {"message_id": self.message_id,
                       "date": datetime.datetime.now().isoformat(),
                       "is_bot": False,
                       **message}

        self.messages.append(new_message)

    def manage_chat(self, message: Message) -> int:
        """ 
         Manage the chat between the user and the bot.
         After a new user's message was created a bot parse the message and response correspondingly.
        Args:
            message (Message): A new message from the user.

        Returns:
            _type_: message_id of the user's message.
        """
        self.create_message(message)
        bot_response = self.bot.get_bot_response(message.get("content"))
        self.create_message(bot_response)
        return self.message_id

    def get_messages(self):
        return self.messages


chat = Chat()
