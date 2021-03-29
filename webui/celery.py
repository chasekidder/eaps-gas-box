from celery import Celery

task_queue = Celery("proj", broker='amqp://localhost', include=['.measure'])


