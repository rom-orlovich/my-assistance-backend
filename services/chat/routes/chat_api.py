

from crypt import methods


from flask import Blueprint, jsonify, request
from services.chat.lib.chat import chat


chat_api = Blueprint("chat_api", __name__, url_prefix="/api/messages")


@chat_api.route("", methods=["GET"])
def get_messages():
    try:
        return chat.get_messages()
    except:
        return []


@chat_api.route("", methods=["POST"])
def post_message():
    message = request.get_json()

    message_id = chat.manage_chat(message)

    response = {
        "message": f'The message with id-{message_id} was created successfully'}
    return jsonify(response)
