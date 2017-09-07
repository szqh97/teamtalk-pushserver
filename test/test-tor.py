#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import pushTasks
from pushTasks import APNs2Tasks 
from pushTasks.APNs2Tasks import *

token = '0b901c2dd4313f82ce1da7b9e6ce13bf6fa02c0de7d91744c99af0e36c89be6a'
headers = {
                'apns-id':'87BC4125-509E-48B9-B34E-1BDEE4D5E369',


}
headers= None
i = 1
payload = {
    'aps': {
            'alert': 'default test{}'.format(i),
            'sound': 'default',
        }
}

APNs2Tasks.apns_push_msg.delay(token, payload, headers)
#APNs2Tasks.apns_push_msg.delay(token, payload, headers)
#APNs2Tasks.apns_push_msg.delay(token, payload, headers)

