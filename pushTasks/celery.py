#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import Celery

app = Celery('pushTasks',
        include=['pushTasks.tasks', 'pushTasks.APNs2Tasks'])

app.config_from_object('pushTasks.celeryconfig')


if __name__ == '__main__':

    app.start()
