#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-18
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93


from flask import Blueprint, render_template, abort, request
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from angel_web.core.json_util import row2json
from angel_web.core.message import *
from traceback import format_exc
from xmlrpc.client import ServerProxy
import json
import re

SessionBuilder = None
task_t = None
tg_t = None


class TaskService(Blueprint):
    """
    Provide task management api for web interface
    """

    def __init__(self, engine, logger, rpc_url):
        global SessionBuilder
        global task_t
        global tg_t
        super(TaskService, self).__init__("task_service", __name__)
        self.engine = engine
        self.logger = logger
        self.rpc_url = rpc_url
        SessionBuilder = sessionmaker(bind=engine)
        metadata = MetaData(engine)
        task_t = Table("task", metadata,
                      Column("id", Integer, primary_key=True),
                      Column('job_id', Integer, ForeignKey('job.id')),
                      Column('group_id', Integer, ForeignKey('task_group.id')),
                      Column('runtime', Integer, nullable=False),
                      Column('worker_id', Integer),
                      Column('done_time', Integer),
                      Column('state', Integer, nullable=False))
        tg_t = Table("task_group", metadata,
                     Column('id', Integer, primary_key=True),
                     Column('group_id', Integer, ForeignKey('job_group.id')),
                     Column('runtime', Integer, nullable=False),
                     Column('done_time', Integer),
                     Column('state', Integer, nullable=False))

    def register_router(self):
        """
        Register router of task service
        """
        @self.route("/data/all_tasks", methods=["GET", "POST"])
        def all_tasks():
            try:
                rows = self.engine.execute(task_t.select().limit(1000).order_by(task_t.c.id)).fetchall()
                return row2json(rows)
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/alive_tasks", methods=["GET", "POST"])
        def alive_tasks():
            try:
                resp = ServerProxy(self.rpc_url).get_alive_tasks()
                if resp["code"] == 0:
                    return json.dumps(resp["content"])
                else:
                    return FailResponse(resp["content"])
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/pending_tasks", methods=["GET", "POST"])
        def pending_tasks():
            try:
                resp = ServerProxy(self.rpc_url).get_pending_tasks()
                if resp["code"] == 0:
                    return json.dumps(resp["content"])
                else:
                    return FailResponse(resp["content"])
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/delete_tasks", methods=["GET", "POST"])
        def delete_tasks():
            ids = request.form["id"]
            where_ = task_t.c.id.in_(ids.split(","))
            try:
                self.engine.execute(task_t.delete().where(where_))
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/all_tgs", methods=["GET", "POST"])
        def all_groups():
            try:
                rows = self.engine.execute(tg_t.select()).fetchall()
                return row2json(rows)
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/delete_tgs", methods=["GET", "POST"])
        def delete_tgs():
            ids = request.form["id"]
            try:
                session = SessionBuilder()
                where_ = task_t.c.group_id.in_(ids.split(","))
                session.execute(task_t.delete().where(where_))
                where_ = tg_t.c.id.in_(ids.split(","))
                session.execute(tg_t.delete().where(where_))
                session.commit()
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                session.rollback()
                return FailResponse(str(e)).to_json()
            finally:
                session.close()
