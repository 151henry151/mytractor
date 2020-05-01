import requests
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from app.models import User
from app.email import send_email
from flask import render_template
import time
import schedule
from flask import Flask
app = Flask(__name__)

def get_harvest_date():
    page_response = requests.get("http://atractor.net/worldnews/index.php", headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86+64 8172.45.0) AppleWebKit/537.36"})
    html = page_response.content
    soup = BeautifulSoup(html, features="html.parser")
    current_date = soup.find('div', { "class" : "WorldInfo" }).contents[-5].text
    return current_date

def email_subscriber(user_id):
    user = User.query.get(user_id)
    current_date = get_harvest_date()
    t = calc_harv_time()
    send_email('[MyTractor] Harvest Notifier',
        sender=app.config['ADMINS'][0], recipients=[user.email],
        text_body=render_template('email/email_subscribers.txt',
        user=user, current_date=current_date, t=t),
        html_body=render_template('email/email_subscribers.html',
        user=user, current_date=current_date, t=t),
        sync=False)


def get_subscribers():
    subs = []
    users = User.query.all()
    for u in users:
        if u.subscriber:
            subs.append(u.id)
    return subs

def notify_subs():
    for user in get_subscribers():
        email_subscriber(user)
    time.sleep(5)

def calc_harv_time():
    right_now_ingame = get_harvest_date().split(", ")[0]
    r_now_ingame = datetime.strptime(right_now_ingame, "%d %b")
    hrvstday = "30 Aug"
    h_day = datetime.strptime(hrvstday, "%d %b")
    days_rem = h_day - r_now_ingame
    mins_rem = days_rem.days * 9.8630137
    t = timedelta(minutes = int(mins_rem))
    t = str(t)
    return t

def sched_notices():
    schedule.every(60).hours.do(notify_subs)


