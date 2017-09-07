#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback
import time

from util.common import install_logger
logger = install_logger(__name__)
from pushTasks import APNs2Tasks

class AndroidPushCmd(object):

    """Docstring for MyClass. """

    def __init__(self, device_token, push_flash, push_data):
        """TODO: to be defined1.

        :device_token: TODO
        :push_flash: TODO
        :push_data: TODO

        """
        self._device_token = device_token
        self._push_flash = push_flash
        self._push_data = push_data

    def _gen_payload(self):
        """TODO: Docstring for function.
        :returns: TODO

        """
        payload = {}
        custom = {}
        extra = {}
        now = int(time.time()*1000)

        title = u"来自私信的消息"

        # construct content
        index = self._push_flash.find(":")
        content = u"您收到一条私信消息"
        if index > 0 :
            content = self._push_flash[index+1:]
        payload["content"] = content
        custom["content"] = content

        try:
            user_data_json = json.loads(self._push_data)
            from_id = user_data_json.get("from_id", None)
            from_uid = user_data_json.get("from_uid", None)
            msg_id =  user_data_json.get("msg_id", None)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        else:
            custom["_tp"] = "p"
            custom["fromid"] = from_id
            custom["msgid"] = msg_id
            custom["title"] = title
            custom["tm"] = now
            extra["custom"] = json.dumps(custom)
            extra["_tp"] = "p"
            extra["tp"] = "p"
            extra["tm"] = now
            payload["createtm"] = now
            payload["devices"] = [self._device_token]
            payload["extra"] = extra
            payload["starttm"] = now
            payload["title"] = title
        logger.info("payload is {}".format(str(payload)))
        return payload
    
    def async_push_msg(self):
        """TODO: Docstring for async_push_msg.
        :returns: TODO

        """
        payload = self._gen_payload()
        APNs2Tasks.android_push_msg.delay(payload)


# for test only
if __name__ == '__main__':
    import requests
    from pushserver_config import *
    token='umengAtAeu1RmmouQo-imx6F93mhMxFqItpYX__UWGGbc7rA_'
    token = "huawei0869542026325143300000392600CN01"
    flash = 'szqh97:Hello world'
    user_data = '{"from_id":1, "from_uid":2, "msg_id":11, "msg_type":1}'

    cmd = AndroidPushCmd(token, flash, user_data)
    cmd.async_push_msg()
