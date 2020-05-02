from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task
from app.tasks import launch_schedule

app = create_app()
cli.register(app)
launch_schedule()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task}
