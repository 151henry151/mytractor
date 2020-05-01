from flask import render_template, current_app
from twilio.rest import Client

def send_text(text_body, recipient, account_sid, auth_token):
    from_ = '+15184127936'
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
               body=text_body,
               from_=from_,
               to=recipient
        )
    print(message.sid)