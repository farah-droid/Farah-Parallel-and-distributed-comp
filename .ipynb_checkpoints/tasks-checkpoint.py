from celery import Celery

# Configure Celery to use RabbitMQ as the message broker
app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

@app.task
def power(n, power):
    return n ** power
