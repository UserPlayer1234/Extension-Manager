import os
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms.responses.readonly']

CLIENT_SECRET = "credentials.json"

def obtain_creds() -> Credentials:
    """Authorizes access to Google Forms by prompting Google login and returns credentials.

        Returns:
            Credentials: Returns existing credentials from token.json or creates new credentials from login
    """

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            app_creds = st.secrets.app_credentials

            client_secret = {
                app_creds.app_type: {
                    "client_id": app_creds.client_id,
                    "project_id": app_creds.project_id,
                    "auth_uri": app_creds.auth_uri,
                    "token_uri": app_creds.token_uri,
                    "auth_provider_x509_cert_url": app_creds.auth_provider_x509_cert_url,
                    "client_secret": app_creds.client_secret,
                    "redirect_uris": app_creds.redirect_uris,
                }
            }

            flow = InstalledAppFlow.from_client_config(
                client_secret, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds