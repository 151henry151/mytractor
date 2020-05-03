from twilio.rest import Client
from flask import current_app

def send_text(text_body, recipient):
    from_ = current_app.config['SYSTEM_PHONE']
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