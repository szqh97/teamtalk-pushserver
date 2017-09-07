#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from pushTasks.celery import app
import logging
import struct
import redis
import json
import requests

import sys
sys.path.append('../')
from util.common import install_logger

from util import Http2APNsClient
from pushserver_config import *

logger = install_logger(__name__)

APNs2Client = Http2APNsClient.APNs2Client
logger = logging.getLogger(__name__)
redis_conn = redis.Redis(host=RedisHost, port=RedisPort, db=RedisDb)
apnsclient = APNs2Client(APNs_Uri, certfile)

@app.task
def apns_ping():
    apnsclient.ping()
    logger.info("apns ping for keeping alive")

@app.task
def apns_push_msg( token, payload, headers):
    if redis_conn.get("invalid_{}".format(token)):
        logger.warn("token [{}] is invalid".format(token))
        return

    resp = apnsclient.push_msg(token, payload, headers)
    if resp.status == 400:
        logger.warn("invalid token: {}".format(token))
        redis_conn.setex("invalid_{}".format(token), 1, InvalidTokenTimout)
    logger.info(u"IOS send msg to apns result:[{}], token[{}], payload:[{}]".format(resp.status, token, str(payload)))


@app.task
def android_push_msg(payload):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload, separators=(',', ': '))
    resp = requests.post(AndroidPushProxy, data, headers=headers)
    logger.info(u"Android send msg result [{}], payload [{}] ".format(resp.status_code, data))

