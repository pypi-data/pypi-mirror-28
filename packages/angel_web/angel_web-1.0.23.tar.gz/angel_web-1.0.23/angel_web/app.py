#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-18
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93

from flask import Flask, request, render_template
from sqlalchemy import create_engine
from angel_web.job import JobService
from angel_web.resource import ResourceService
from angel_web.task import TaskService
from angel_web.log import LogService
from angel_web.core.ftp_client import FTPClient
from angel_web.core import config_util
from flask_socketio import SocketIO
from logging import config
from traceback import format_exc
import os
import logging

ETC_PATH = '/etc/angel/web/'
HTML_FOLDER = "html"
STATIC_FOLDER = "static"

def serve_forever(debug=False):
    # setup logger
    logger_config_path = os.path.join(ETC_PATH, "logger.conf")
    logging.config.fileConfig(logger_config_path)
    if debug:
        logger = logging.getLogger("debug")
    else:
        logger = logging.getLogger("release")
    # loading setting
    config_path = os.path.join(ETC_PATH, "web.conf")
    if not os.path.isfile(config_path):
        logger.error("configuration file %s not exist" % config_path)
    try:
        config = config_util.parse(config_path, "web")
        host = config["host"]
        port = int(config["port"])
        fs_host = config["fs_host"]
        fs_port = int(config["fs_port"])
        fs_timeout = int(config["fs_timeout"])
        fs_name = config["fs_name"]
        fs_pwd = config["fs_password"]
        fs_buffer_size = int(config["fs_buffer_size"])
        fs_script_path = config["fs_script_path"]
        fs_log_path = config["fs_log_path"]
        local_script_path = config["local_script_path"]
        master_rpc_url = config["rpc_url"]
        db_url = config["db_url"]
        max_overflow = int(config["max_overflow"])
    except Exception as e:
        logger.error("config file '%s' error: %s" %(config_path, format_exc()))
        raise
    try:
        # create work directory
        if not os.path.isdir(local_script_path):
            os.makedirs(local_script_path)
        # init db engine
        engine = create_engine(db_url, max_overflow=max_overflow)
        # create app and register router
        app = Flask(__name__, template_folder=HTML_FOLDER, static_folder=STATIC_FOLDER, static_url_path="")
        # init filesystem client
        fs_client = FTPClient(fs_host, fs_port, fs_timeout, fs_name, fs_pwd, fs_buffer_size)
        # init job service
        job_service = JobService(engine, logger, master_rpc_url, fs_client, fs_script_path, local_script_path)
        job_service.register_router()
        app.register_blueprint(job_service)
        # init resource service
        resource_service = ResourceService(engine, logger, master_rpc_url)
        resource_service.register_router()
        app.register_blueprint(resource_service)
        # init task service
        task_service = TaskService(engine, logger, master_rpc_url)
        task_service.register_router()
        app.register_blueprint(task_service)
        # init log service
        log_service = LogService(logger, master_rpc_url, fs_client, fs_log_path)
        log_service.register_router()
        app.register_blueprint(log_service)
        # setup router of html pages
        register_router(app)
        # init websocket
        socketio = SocketIO(app)
        log_service.register_socket_router(socketio)
        # run the service
        socketio.run(app, host, port)
    except:
        logger.error(format_exc())
        raise


def register_router(app):
    """
    Register router of the web service
    """
    @app.route("/", methods=["GET", "POST"])
    @app.route("/html/", methods=["GET", "POST"])
    def index():
        return render_template("index.html")

    @app.route("/html/<page>", methods=["GET"])
    def send_page(page):
        return render_template(page, **request.args.to_dict())

    @app.route("/static/<path>", methods=["GET", "POST"])
    def send_static_file(path):
        return app.send_static_file(path)

