

from crypt import methods
from flask_cors import CORS, cross_origin
from flask_restful import reqparse, Resource, request
from flask import Blueprint, jsonify

from Calendar import Calendar
from Chat import chat


chat_api = Blueprint("chat_api", __name__, url_prefix="/api/messages")
# CORS(chat_api)
# CORS(chat_api, resources={
#     r"/api/*": {"origins": "*"}}, supports_credentials=True)

# class ChatAPI():
#     def get(self):
#         try:
#             return chat.get_messages()
#         except:
#             return []

#     def delete(self):
#         pass

#     def post(self):
#         message = messages_args.parse_args()
#         message_id = chat.manage_chat(message)

#         return {"message": f'The message with id-{message_id} was created successfully'}, 201


@chat_api.route("", methods=["GET"])
def get_messages():
    try:
        return chat.get_messages()
    except:
        return []


# @cross_origin(supports_credentials=True)
@chat_api.route("", methods=["POST"])
def post_message():
    message = request.get_json()

    message_id = chat.manage_chat(message)

    response = {
        "message": f'The message with id-{message_id} was created successfully'}
    return jsonify(response)
# messages_args = reqparse.RequestParser()
# messages_args.add_argument("content", type=str, required=True)
# messages_args.add_argument("user_id", type=int)
# messages_args.add_argument("is_bot", type=bool)
