
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from services.chat.routes.chat_api import chat_api
from services.auth.auth import auth
load_dotenv()


app = Flask(__name__)
api = Api(app)
app.secret_key = getenv("SECRET_KEY")


app.register_blueprint(chat_api)
app.register_blueprint(auth)
CORS(app, resources={
    r"/api/*": {"origins": "*"}}, supports_credentials=True)


if __name__ == "__main__":
    app.run(debug=True)
