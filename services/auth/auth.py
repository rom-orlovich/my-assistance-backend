from google_auth_oauthlib.flow import Flow

from flask import Blueprint, Response, session, redirect, request
import pathlib
from os import path


# Initialize the flow in order to connect to google api.
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


auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.route("/authorize", methods=["GET"])
def authorize() -> Response:
    """
    The callback the executed after the user will login to his google account.
    """

    code = request.args.get("code")
    # Get the token of the login user.
    flow.fetch_token(code=code)

    # save user's credentials in session.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect("http://localhost:3000")
