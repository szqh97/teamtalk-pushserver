#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hyper import HTTP20Connection, tls
import struct
import traceback
import sys
import json
import logging
logger = logging.getLogger(__name__)
sys.path.append('../')

import pushserver_config

class APNs2Client(object):

    """Docstring for APNS2Client. """

    def __init__(self, uri, certfile):
        self.conn = None
        """
        :uri: apns push uri
        :certfile: cert file
        """
        self._uri = uri
        self._certfile = certfile
        self._conn = HTTP20Connection(self._uri, ssl_context=
                tls.init_context(cert=self._certfile))

    def ping(self):
        """
        :returns: TODO
        """
        try:
            self._conn.ping(struct.pack('l', 0))
        except Exception as e:
            logger.warn("reconnecting APNs server")
            self._conn = HTTP20Connection(self._uri, ssl_context=
                tls.init_context(cert=self._certfile))
            logger.error(traceback.format_exc())

    def push_msg(self, token, payload, headers):
        """
        http2 apns push msg. 
        this function should be excuted in celery tasker.

        :token: device token
        :payload:  payload, json object
        :headers: http2 headers contains apns-id jsonobject
        :returns: response

        """
        self.ping()
        try:
            self._conn.request('POST', '/3/device/{}'.format(token), body=json.dumps(payload), headers = headers)
            resp = self._conn.get_response()
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        else:
            return resp
        

### for test only
if __name__ == '__main__':
    c =APNs2Client('api.development.push.apple.com:443', '/Users/li_yun/work/cert.pem')
    token = '0b901c2dd4313f82ce1da7b9e6ce13bf6fa02c0de7d91744c99af0e36c89be6a'

    headers = {
	'apns-id':'87BC4125-509E-48B9-B34E-1BDEE4D5E369',
    }
    for i in range(100):
	
	payload = {
	    'aps': {
		'alert': 'default test{}'.format(i),
		'sound': 'default',
	    }
	}

        r = c.push_msg(token, payload, headers)
        print r.status
