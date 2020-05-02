from twilio.rest import Client
from flask import current_app

def send_text(text_body, recipient):
    from_ = '+15184127936'
    account_sid = current_app.config['TWILIO_SID']
    auth_token = current_app.config['TWILIO_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
               body=text_body,
               from_=from_,
               to=recipient
        )
    print(message.sid)