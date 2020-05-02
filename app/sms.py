from twilio.rest import Client

def send_text(text_body, recipient):
    from_ = '+15184127936'
    account_sid = app.config['TWILIO_SID']
    auth_token = app.config['TWILIO_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
               body=text_body,
               from_=from_,
               to=recipient
        )
    print(message.sid)