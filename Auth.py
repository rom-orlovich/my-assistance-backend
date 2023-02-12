from google_auth_oauthlib.flow import Flow

from flask_restful import Resource, request
from flask import session, redirect
import pathlib
from os import path, getenv


CLIENT_SECRETS_FILE = "client_secret.json"
scopes = ["https://www.googleapis.com/auth/userinfo.email",
          "https://www.googleapis.com/auth/userinfo.profile", "openid", "https://www.googleapis.com/auth/calendar"]

flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE, scopes=scopes,
    redirect_uri="http://localhost:5000/api/auth/authorize")

# set the path to where the .json file you got Google console is
client_secrets_file = path.join(pathlib.Path(
    __file__).parent, "client_secret.json")


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


class Auth(Resource):
    def get(self):
        authorization_response = request.url
        code = request.args.get("code")

        t = flow.fetch_token(code=code)
        credentials = flow.credentials

        session['credentials'] = credentials_to_dict(credentials)

        return redirect("http://localhost:3000")
