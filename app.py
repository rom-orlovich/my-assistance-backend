from flask import Flask, request, redirect, session
from flask_restful import Resource, Api, reqparse
# import google.oauth2.credentials
from Chat import chat
from flask_cors import CORS
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from os import path

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
