#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback

from pushTasks import APNs2Tasks
from util.common import install_logger
logger = install_logger(__name__)

class IOSPushCmd(object):

    """Docstring for IOSPushCmd. """

    def __init__(self, device_token, push_flash, push_data):
        self._push_flash = push_flash
        self._token = device_token
        self._push_data = push_data

    def _gen_payload(self):
        """TODO: Docstring for _gen_payload.
        :returns: payload 
        """
        payload = {}
        payload['_tp'] = 'p'
        try:
            user_data_json = json.loads(self._push_data)
            from_id = user_data_json.get("from_id", None)
            from_uid = user_data_json.get("from_uid", None)
            msg_type = user_data_json.get("msg_type", None)
            msg_id =  user_data_json.get("msg_id", None)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        else:
            custom = {}
            if from_id is not None:     custom["from_id"] = from_id
            if from_uid is not None:    custom["from_uid"] = from_uid
            if msg_type is not None:    custom["msg_type"] = msg_type
            payload["custom"] = json.dumps(custom)
            payload["msg_id"] = msg_id

            aps ={"badge":1, "sound": "bingdong.tiff", "alert":{"body": self._push_flash}}
            payload["aps"] = aps
        logger.info("payload is {}".format(str(payload)))
        return payload

    def async_push_msg(self):
        """TODO: Docstring for asyn_push_msg.
        :returns: TODO

        """
        payload = self._gen_payload()
        APNs2Tasks.apns_push_msg.delay(self._token, payload, None)
        pass


### for test only
if __name__ == "__main__":
    token = '0b901c2dd4313f82ce1da7b9e6ce13bf6fa02c0de7d91744c99af0e36c89be6a'
    flash = 'szqh97:Hello world'
    user_data = '{"from_id":1, "from_uid":2, "msg_id":11, "msg_type":1}'

    cmd = IOSPushCmd(token, flash, user_data)
    print cmd._gen_payload()
    cmd.async_push_msg()
