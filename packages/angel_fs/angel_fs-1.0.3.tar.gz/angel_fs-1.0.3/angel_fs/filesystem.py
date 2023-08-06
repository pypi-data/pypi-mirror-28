#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-03
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from logging import config
from angel_fs.utils import config_util
from traceback import format_exc
import logging
import os
import sys

ETC_PATH = '/etc/angel/fs/'

def serve_forever(debug=False):
    # setup logger
    logger_config_path = os.path.join(ETC_PATH, "logger.conf")
    logging.config.fileConfig(logger_config_path)
    if debug:
        logger = logging.getLogger("debug")
    else:
        logger = logging.getLogger("release")
    # load settings
    config_path = os.path.join(ETC_PATH, "fs.conf")
    if not os.path.isfile(config_path):
        logger.error("configuration file %s not exist" % config_path)
    try:
        config = config_util.parse(config_path, "filesystem")
        host = config["host"]
        port = int(config["port"])
        root_name = config["root_name"]
        root_pwd = config["root_password"]
        root_path = config["root_path"]
        log_name = config["log_name"]
        log_pwd = config["log_password"]
        log_path = config["log_path"]
        script_name = config["script_name"]
        script_pwd = config["script_password"]
        script_path = config["script_path"]
    except Exception as e:
        logger.error("config file '%s' error: %s" %(config_path, format_exc()))
        raise
    if not os.path.isdir(root_path):
        os.mkdir(root_path)
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    if not os.path.isdir(script_path):
        os.mkdir(script_path)
    # initialize ftp server
    authorizer = DummyAuthorizer()
    authorizer.add_user(root_name, root_pwd, root_path, perm="elradfmwMT")
    authorizer.add_user(log_name, log_pwd, log_path, perm="elradfmwMT")
    authorizer.add_user(script_name, script_pwd, script_path, perm="elradfmwMT")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((host, port), handler)
    # startup ftp service
    server.serve_forever()
