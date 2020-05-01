from app import create_app
from app.harvest import notify_subs, sched_notices
notify_subs()
print("looks like it is working")
sched_notices()