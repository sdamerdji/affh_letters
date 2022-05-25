import os.path

from typing import List, Tuple
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import base64
from textwrap import dedent

"""
Credit for this code goes to Sid https://github.com/YIMBYdata/rhna-apr-emails/blob/main/gmail.py
"""

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
]

def format_recipients_list(emails: List[Tuple[str, str]]) -> str:
    return ', '.join(f'{name} <{email}>' for name, email in emails)


def make_email(
    to: List[Tuple[str, str]],
    cc: List[Tuple[str, str]],
    subject: str,
    body: str,
    attachments: List[Path]
) -> MIMEMultipart:
    message = MIMEMultipart('mixed')
    message['To'] = format_recipients_list(to)
    message['CC'] = format_recipients_list(cc)
    message['From'] = 'Salim Damerdji <sdamerdji1@gmail.com>'
    message['Subject'] = subject

    # Convert to HTML
    paragraphs = body.split('\n\n')
    html_body = "\n".join(f"<p>{para}</p>" for para in paragraphs)
    plain_body = body.replace('<br>', '')

    # part_1 = MIMEText(plain_body, 'plain')
    part_2 = MIMEText(html_body, 'html')

    # message.attach(part_1)
    message.attach(part_2)

    for attachment_name, attachment in attachments:
        attachment_part = MIMEBase("application", "octet-stream")
        attachment_part.set_payload(attachment.read_bytes())
        encode_base64(attachment_part)

        attachment_part.add_header("Content-Disposition", f"attachment; filename= {attachment_name}")
        message.attach(attachment_part)

    return message

def send_email(message: MIMEMultipart) -> None:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    message_encoded = {
        'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
    }

    service.users().messages().send(userId='me', body=message_encoded).execute()

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    message = make_email(
        to=[('Salim Damerdji', 'sdamerdji1@gmail.com')],
        cc=[],
        subject='Test from Gmail API!',
        body=dedent(
            """\
            Hello,
            This is an email test.
            Thanks so much,<br>
            Salim
            """
        ),
        attachments=[Path("./letters/Atherton.pdf")]
    )

    send_email(message)


if __name__ == '__main__':
    main()