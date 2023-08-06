#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-27
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93

from flask_socketio import disconnect, emit, join_room, rooms
from flask import Blueprint, request, redirect
from angel_web.core.json_util import row2json
from angel_web.core.message import *
from traceback import format_exc
from threading import Lock
from xmlrpc.client import ServerProxy
from traceback import format_exc
import os

NAMESPACE = "/log"
EVENT = "log"


class LogService(Blueprint):
    """
    Provide log management api for web interface
    Also provide log upload interface for executor
    """

    def __init__(self, logger, rpc_url, fs_client, fs_log_path):
        super(LogService, self).__init__("log_service", __name__)
        self.logger = logger
        self.rpc_url = rpc_url
        self.fs_client = fs_client
        self.fs_log_path = fs_log_path
        self.task_ids = {}
        self.lock = Lock()

    def register_router(self):
        """
        Register router of log service
        """
        @self.route("/log/upload", methods=["GET", "POST"])
        def upload_log():
            task_id = request.form.get("task_id")
            log = request.form.get("log")
            if task_id in self.task_ids:
                emit(EVENT, {"data": log}, namespace=NAMESPACE, room=task_id)
                return RESPONSE_SUCCESS
            else:
                return RESPONSE_FAIL

    def register_socket_router(self, socketio):
        @socketio.on("connect", namespace=NAMESPACE)
        def on_connect():
            task_id = request.args.get("tid")
            if task_id is None:
                disconnect()
            self.logger.debug("--connected: tid=" + task_id)
            # read from filesystem if the log exist in ftp server
            try:
                path = os.path.join(self.fs_log_path, task_id)
                if self.fs_client.isfile(path):
                    self.fs_client.read(self._emit_log(socketio, task_id), self.fs_log_path, task_id)
                    return
            except:
                self.logger.warn(format_exc())
            # rpc master for sending log command
            try:
                resp = ServerProxy(self.rpc_url).add_log(int(task_id))
                if resp["code"] == 0:
                    join_room(task_id)
                    with self.lock:
                        counter = self.task_ids.get(task_id, 0)
                        self.task_ids[task_id] = counter + 1
                    return
                else:
                    message = resp["content"]
            except Exception as e:
                message = str(e)
            msg = "add log monitor fail caused by " + message
            self.logger.warn(msg)
            emit(EVENT, {"data": "<font color='red' size='5'>%s</font>" % msg})

        @socketio.on("disconnect", namespace=NAMESPACE)
        def on_disconnect():
            task_id = request.args.get("tid")
            if task_id is None:
                return RESPONSE_EMPTY_FIELD
            self.logger.debug("--disconnected: tid=" + task_id)
            with self.lock:
                counter = self.task_ids.get(task_id)
                if counter and counter > 1:
                    self.task_ids[task_id] = counter - 1
                elif counter is not None:
                    del self.task_ids[task_id]

        @socketio.on("close_req", namespace=NAMESPACE)
        def on_close():
            disconnect()

    def _emit_log(self, socketio, tid):
        """
        Helper method for sending log to web browser through websocket
        """
        def func(message):
            message = message.decode("utf8")
            emit(EVENT, {"data": message}, namespace=NAMESPACE)
        return func
