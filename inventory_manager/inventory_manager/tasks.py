# -*- coding: utf-8 -*-
from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://localhost//')


@app.task
def add(x, y):
    return x + y
