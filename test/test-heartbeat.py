#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from IM import BaseDefine_pb2
from IM import Server_pb2
from IM import Other_pb2
from pduCommon import ImPdu
import socket
import time

h = Other_pb2.IMHeartBeat()
h.SerializeToString()
pdu = ImPdu.ImPdu()
pdu.command_id  = BaseDefine_pb2.CID_OTHER_HEARTBEAT
pdu.service_id = BaseDefine_pb2.SID_OTHER
pdu.SerializeToString()
buf = pdu.SerializeToString()

cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
cli.connect(('127.0.0.1', 65000))
for i in xrange (80000):
    cli.send(buf)
    s = cli.recv(16)
    print len(s)
time.sleep(20)
for i in xrange(10):
    cli.send(buf)
