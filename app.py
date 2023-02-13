from unicodedata import name
from flask import Flask
from flask_restful import Api


from flask_cors import CORS


from dotenv import load_dotenv
from os import getenv
from ChatAPI import ChatAPI
from Auth import Auth
load_dotenv()


app = Flask(__name__)
api = Api(app)
app.secret_key = getenv("SECRET_KEY")
api.add_resource(ChatAPI, "/api/messages")
api.add_resource(Auth, "/api/auth", "/api/auth/authorize")

cors = CORS(app, resources={
    r"/api/*": {"origins": "*"}}, supports_credentials=True)


if __name__ == "__main__":
    app.run(debug=True)
