from flask import Flask
from flask_restful import Resource, Api, reqparse
from Chat import chat
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
messages_args = reqparse.RequestParser()
messages_args.add_argument("content", type=str, required=True)
messages_args.add_argument("user_id", type=int)
messages_args.add_argument("is_bot", type=bool)


class ChatMessage(Resource):
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


api.add_resource(ChatMessage, "/api/messages")

if __name__ == "__main__":
    app.run(debug=True)
