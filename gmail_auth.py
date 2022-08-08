import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
]

"""
Credit for this code goes to Sid https://github.com/YIMBYdata/rhna-apr-emails/blob/main/gmail_auth.py
"""

def main():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./letter_data/token.json'):
        creds = Credentials.from_authorized_user_file('./letter_data/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_462780577837-jl1ifrder7h2u0e8kmrrjtj337dt9p1m.apps.googleusercontent.com.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./letter_data/token.json', 'w') as token:
            token.write(creds.to_json())


if __name__ == '__main__':
    main()