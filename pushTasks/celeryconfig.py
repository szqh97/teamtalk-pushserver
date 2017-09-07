#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timedelta

BROKER_URL = 'redis://127.0.0.1:6379/8'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/8'
CELERY_IMPORTS = ('pushTasks')

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERYBEAT_SCHEDULE = {
    'APNsPingTask' : {
            'task':'pushTasks.APNs2Tasks.apns_ping',
            'schedule':timedelta(seconds=59),
            'args':()
                                        
            }

}
