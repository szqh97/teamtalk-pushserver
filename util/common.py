#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

def install_logger(name):
    logger = logging.getLogger(name)
    hdlr = logging.FileHandler('/dev/stdout')
    formatter = logging.Formatter('%(asctime)s %(levelname)s (%(filename)s:%(lineno)d) [%(funcName)s] %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    return logger
