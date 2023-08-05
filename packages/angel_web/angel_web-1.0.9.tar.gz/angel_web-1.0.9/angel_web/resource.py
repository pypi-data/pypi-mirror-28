#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-18
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93


from flask import Blueprint, request
from angel_web.core.message import *
from traceback import format_exc
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from angel_web.core.json_util import row2json
from xmlrpc.client import ServerProxy
import json

SessionBuilder = None
worker_t = None
wg_t = None


class ResourceService(Blueprint):
    """
    Provide resource management api for web interface
    """

    def __init__(self, engine, logger, rpc_url):
        global SessionBuilder
        global worker_t
        global wg_t
        super(ResourceService, self).__init__("resource_service", __name__)
        self.engine = engine
        self.logger = logger
        self.rpc_url = rpc_url
        SessionBuilder = sessionmaker(bind=engine)
        metadata = MetaData(engine)
        worker_t = Table("worker", metadata,
                         Column('id', Integer, primary_key = True),
                         Column('group_id', Integer, ForeignKey('worker_group.id')),
                         Column('login_time', Integer),
                         Column('desc', String(128)))
        wg_t = Table("worker_group", metadata,
                     Column("id", Integer, primary_key = True),
                     Column("name", String(64), nullable = False),
                     Column("desc", String(128)))

    def register_router(self):
        """
        Register router of the resource service
        """
        @self.route("/data/all_wgs", methods=["GET", "POST"])
        def all_worker_groups():
            try:
                rows = self.engine.execute(wg_t.select()).fetchall()
                return row2json(rows)
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/update_wgs", methods=["GET", "POST"])
        def update_worker_groups():
            # obtain changes worker groups
            items = json.loads(request.form["json"])
            # vertify the input data
            for item in items:
                if item.get("id") == '':
                    item["id"] = None
                if not item.get("name"):
                    return RESPONSE_EMPTY_FIELD
            # save into db
            try:
                session = SessionBuilder()
                for item in items:
                    if "addFlag" in item:
                        session.execute(wg_t.insert(), item)
                    else:
                        where_ = wg_t.c.id==item.pop("id")
                        session.execute(jg_t.update().where(where_), item)
                session.commit()
            except Exception as e:
                self.logger.warn(format_exc())
                session.rollback()
                return FailResponse(str(e)).to_json()
            finally:
                session.close()
            return RESPONSE_SUCCESS

        @self.route("/data/delete_wgs", methods=["GET", "POST"])
        def delete_worker_groups():
            ids = request.form["id"]
            where_ = wg_t.c.id.in_(ids.split(","))
            try:
                self.engine.execute(wg_t.delete().where(where_))
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/all_workers", methods=["GET", "POST"])
        def all_workers():
            try:
                rows = self.engine.execute(worker_t.select()).fetchall()
                return row2json(rows)
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/update_workers", methods=["GET", "POST"])
        def update_workers():
            # obtain changes workers
            items = json.loads(request.form["json"])
            # vertify the input data
            for item in items:
                if not item.get("id"):
                    return RESPONSE_EMPTY_FIELD
                if item.get("group_id") == '':
                    item["group_id"] = None
            # update worker group
            try:
                session = SessionBuilder()
                for item in items:
                    where_ = worker_t.c.id==item.pop("id")
                    session.execute(worker_t.update().where(where_), item)
                session.commit()
            except Exception as e:
                self.logger.warn(format_exc())
                session.rollback()
                return FailResponse(str(e)).to_json()
            finally:
                session.close()
            return RESPONSE_SUCCESS

        @self.route("/data/delete_workers", methods=["GET", "POST"])
        def delete_workers():
            ids = request.form("id")
            where_ = worker_t.c.id.in_(ids.split(","))
            try:
                self.engine.execute(worker_t.delete().where(where_))
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/alive_workers", methods=["GET", "POST"])
        def alive_workers():
            # obtain worker list from master by rpc
            try:
                resp = ServerProxy(self.rpc_url).all_alive_workers()
                if resp["code"] == 0:
                    return json.dumps(resp["content"])
                else:
                    return FailResponse(resp["content"])
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/resource/off_worker", methods=["GET", "POST"])
        def off_workers():
            return RESPONSE_SUCCESS
