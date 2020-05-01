import json
import sys
import time
from flask import render_template
from rq import get_current_job
from app import create_app, db
from app.models import User, Post, Task
from app.email import send_email
from app.sms import send_text
from app.harvest import game_date, time_until_harvest
from datetime import timedelta

app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,
                         'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_posts)

        send_email('[MyTractor] Your blog posts',
                sender=app.config['ADMINS'][0], recipients=[user.email],
                text_body=render_template('email/export_posts.txt', user=user),
                html_body=render_template('email/export_posts.html',
                                          user=user),
                attachments=[('posts.json', 'application/json',
                              json.dumps({'posts': data}, indent=4))],
                sync=True)
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())


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
                  recipient=phone,
                  account_sid=app.config['TWILIO_SID'],
                  auth_token=app.config['TWILIO_TOKEN'])


def launch_schedule():
    launch_delay = timedelta(minutes = 30)
    time_remaining = time_until_harvest()
    if time_remaining <= launch_delay:
        schedule_notices()



def schedule_notices():
    schedule.every(60).hours.do(email_subscribers)
    schedule.every(60).hours.do(text_subscribers)
