#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
import json

from tornado.tcpserver import TCPServer
from tornado.gen import coroutine, Task, Return
from tornado.concurrent import Future
from tornado.ioloop import IOLoop
from tornado import iostream

from util import common
from pduCommon.ImPdu import PDU_HEAD_LEN, ImPdu

from IM import BaseDefine_pb2
from IM import Server_pb2

from IOSPushSession import IOSPushCmd
from AndroidPushSession import AndroidPushCmd

global logger
logger = common.install_logger(__name__)

class PushConn(object):

    """Docstring for PushConn. """

    def __init__(self, stream, address):
        self._stream = stream
        self._address = address

    @coroutine
    def on_close(self):
        try:
            logger.debug("on close, {0[0]}:{0[1]}".format(self._address))
            yield []
        except Exception as e:
            pass

    @coroutine
    def on_connect(self):
        logger.debug("on connect, {0[0]}:{0[1]}".format(self._address))
        yield self.dispatch()
        return

    @coroutine
    def dispatch(self):
        """
        :returns: TODO

        """
        while True:
            try:
                h_buf = yield Task(self._stream.read_bytes, PDU_HEAD_LEN)
                pdu = ImPdu()
                pdu.ParseHeaderFromBuffer(h_buf)

                if pdu.length > 16:
                    msg_buf = yield Task(self._stream.read_bytes, pdu.length - PDU_HEAD_LEN)
                    pdu.msg = msg_buf
                r = yield Task(self.handle_pdu, pdu)

            except (iostream.StreamClosedError,
                    iostream.UnsatisfiableReadError):
                print traceback.format_exc()
                return
            except Exception as e:
                print traceback.format_exc()
                return 

    @coroutine
    def handle_pdu(self, pdu):
        if pdu.command_id == BaseDefine_pb2.CID_OTHER_HEARTBEAT:
            self._handleHeartBeat(pdu)
        elif pdu.command_id == BaseDefine_pb2.CID_OTHER_PUSH_TO_USER_REQ:
            self._handlePushMsg(pdu)
        else:
            logger.warn("push server recv undefined msg, command_id is {}".format(pdu.command_id))
        pass

    @coroutine
    def _handleHeartBeat(self, pdu):
        logger.debug("_handleHeartBeat")
        try:
            if self._stream.closed():
                logger.warn ("socket is closed")
                return
            r= yield Task(self._stream.write, pdu.SerializeToString())
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
    
    @coroutine
    def _handlePushMsg(self, pdu):
        logger.info("_handlePushMsg")
        msg_buf = pdu.msg
        msg = Server_pb2.IMPushToUserReq.FromString(msg_buf)
        push_flash = msg.flash
        push_data = msg.data
        logger.info(u"push_flash:[{}], push_data:[{}]".format(push_flash, push_data))

        respmsg = Server_pb2.IMPushToUserRsp()

        def _push_proc(user_token):
            assert(isinstance(user_token, BaseDefine_pb2.UserTokenInfo))
            idx = user_token.token.find(":")
            token = user_token.token[idx+1:]
            push_result = respmsg.add()
            push_result.Clear()
            push_result.user_token = token
            push_result.result_code = 0
            if user_token.user_type == BaseDefine_pb2.CLIENT_TYPE_IOS:
                ios_push_cmd = IOSPushCmd(token, push_flash, push_data)
                ios_push_cmd.async_push_msg()
            elif user_token.user_type == BaseDefine_pb2.CLIENT_TYPE_ANDROID:
                android_push_cmd = AndroidPushCmd(token, push_flash, push_data)
                android_push_cmd.async_push_msg()

        map(_push_proc, msg.user_token_list)
        pdu = ImPdu()
        pdu.setMsg(respmsg.SerializeToString())
        pdu.setServiceId(BaseDefine_pb2.SID_OTHER)
        pdu.setCommandId(BaseDefine_pb2.CID_OTHER_PUSH_TO_USER_RSP)
        r = yield Task(self._strea.write, pdu.SerializeToString())
        

