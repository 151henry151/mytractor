from app.sms import send_text
from app.harvest import game_date, time_until_harvest
from datetime import timedelta
import schedule
from app.email import send_email


def get_subscribers():
    subscribers = []
    users = User.query.all()
    for u in users:
        if u.subscriber:
            subscribers.append(u.id)
    return subscribers


def get_phone_subscribers():
    phone_subscribers = []
    users = User.query.all()
    for u in users:
        if u.phone_subscriber:
            phone_subscribers.append(u.id)
    return phone_subscribers


def email_subscribers():
    for user_id in get_subscribers():
        user = User.query.get(user_id)
        game_time = game_date().strftime("%d %b")
        time_left = str(time_until_harvest())
        send_email('[MyTractor] Harvest Notifier',
            sender=app.config['ADMINS'][0], recipients=[user.email],
            text_body=render_template('email/email_subscribers.txt',
            user=user, game_date=game_time, time_until_harvest=time_left),
            html_body=render_template('email/email_subscribers.html',
            user=user, game_date=game_time, time_until_harvest=time_left),
            sync=False)

def text_subscribers():
    for user_id in get_phone_subscribers():
        user = User.query.get(user_id)
        game_time = game_date().strftime("%d %b")
        time_left = str(time_until_harvest())
        phone = user.phone
        text_body = render_template('sms/notify_harvest.txt',
                                    user=user, game_date=game_time,
                                    time_remaining=time_left)
        send_text(text_body=text_body,
                  recipient=phone)


def launch_schedule():
    schedule.every(1).minutes.do(check_if_time_to_schedule_notices)
    schedule.run_pending()

def check_if_time_to_schedule_notices():
    launch_delay = timedelta(minutes = 30)
    time_remaining = time_until_harvest()
    if time_remaining <= launch_delay:
        send_text(text_body='Schedule launching',
                  recipient=app.config[ADMIN_PHONE])
        return schedule.CancelJob
        schedule_notices()
    else:
        send_text(text_body='Schedule launcher checked and it is not time to launch the schedule yet.',
                  recipient=app.config[ADMIN_PHONE])

def schedule_notices():
    schedule.every(60).hours.do(email_subscribers)
    schedule.every(60).hours.do(text_subscribers)
    schedule.run_pending()