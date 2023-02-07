

from flask_restful import reqparse, Resource
from Calendar import Calendar
from Chat import chat


class ChatAPI(Resource):
    def get(self):
        try:
            return chat.get_messages()
        except:
            return []

    def delete(self):
        pass

    def post(self):
        message = messages_args.parse_args()
        message_id = chat.manage_chat(message)

        return {"message": f'The message with id-{message_id} was created successfully'}, 201


messages_args = reqparse.RequestParser()
messages_args.add_argument("content", type=str, required=True)
messages_args.add_argument("user_id", type=int)
messages_args.add_argument("is_bot", type=bool)
