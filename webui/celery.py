from celery import Celery

task_queue = Celery(broker='amqp://localhost')


