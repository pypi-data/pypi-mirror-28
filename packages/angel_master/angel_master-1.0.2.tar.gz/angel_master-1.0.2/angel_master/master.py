#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-11-27
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93

from angel_master.resource_manager import ResourceManager
from angel_master.scheduler import Scheduler
from angel_master.jobstore import JobStore
from angel_master.scheduler_rule.rand import RandomRule
from angel_master.core import config_util
from angel_master.api.rpc_server import XMLRPCServer
from sqlalchemy import create_engine
from traceback import format_exc
import logging
import logging.config
import os

ETC_PATH = "/etc/angel/master/"

scheduler = None
resource_manager = None
jobstore = None
logger = None
rpc_server = None


def serve_forever(debug=False):
    global scheduler
    global resource_manager
    global jobstore
    global logger
    global rpc_server
    # setup logger
    logger_config_path = os.path.join(ETC_PATH, "logger.conf")
    logging.config.fileConfig(logger_config_path)
    if debug:
        logger = logging.getLogger("debug")
    else:
        logger = logging.getLogger("release")
    # load setting
    config_path = os.path.join(ETC_PATH, "master.conf")
    if not os.path.isfile(config_path):
        logger.error("configuration file %s not exist" % config_path)
    try:
        # import settings
        config = config_util.parse(config_path, 'master')
        name = config['name']
        pwd = config['password']
        host = config["host"]
        port = int(config["port"])
        db_url = config["db_url"]
        max_overflow = int(config["max_overflow"])
        heartbeat_loop_time = int(config["heartbeat_loop_time"])
        worker_timeout = int(config["worker_timeout"])
        schedule_timeout = int(config["schedule_timeout"])
        schedule_loop_time = int(config["schedule_loop_time"])
    except Exception as e:
        logger.error("config file '%s' error: %s" %(config_path, format_exc()))
        raise
    # init db engine
    engine = create_engine(db_url, max_overflow=max_overflow)
    # init jobstore
    jobstore = JobStore(engine, logger)
    # init resource manager
    resource_manager = ResourceManager(logger, heartbeat_loop_time, worker_timeout, engine, name, pwd)
    # init scheduler
    rule = RandomRule()
    scheduler = Scheduler(jobstore, resource_manager, rule, logger, schedule_timeout, schedule_loop_time)
    # init rpc service
    rpc_server = XMLRPCServer(host, port, logger, scheduler, resource_manager)
    # start services of Master
    _start()


def _start():
    # startup resource manager
    resource_manager.start()
    # start up scheduler
    scheduler.start()
    # start up rpc service
    rpc_server.start()


def _stop():
    # stop rpc service
    rpc_server.stop()
    # stop scheduler
    scheduler.stop()
    # stop resource manager
    resource_manager.stop()
