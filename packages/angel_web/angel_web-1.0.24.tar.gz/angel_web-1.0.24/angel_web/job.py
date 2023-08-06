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
import os

SessionBuilder = None
job_t = None
jg_t = None
jd_t = None


class JobService(Blueprint):
    """
    Provide job management api for web interface
    """

    def __init__(self, engine, logger, rpc_url, fs_client, fs_script_path, local_script_path):
        global SessionBuilder
        global job_t
        global jg_t
        global jd_t
        super(JobService, self).__init__("job_service", __name__)
        self.engine = engine
        self.logger = logger
        self.rpc_url = rpc_url
        self.fs_client = fs_client
        self.fs_script_path = fs_script_path
        self.local_script_path = local_script_path
        SessionBuilder = sessionmaker(bind=engine)
        metadata = MetaData(engine)
        job_t = Table("job", metadata,
                      Column("id", Integer, primary_key=True),
                      Column('group_id', Integer, ForeignKey('job_group.id')),
                      Column('name', String(64), nullable=False),
                      Column('desc', String(128)),
                      Column('worker_gid', Integer),
                      Column('trigger', String(32)),
                      Column('running_timeout', Integer, nullable=False))
        jg_t = Table("job_group", metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String(64), nullable=False),
                     Column('desc', String(128)),
                     Column('first_job_id', Integer, ForeignKey('job.id')))
        jd_t = Table("job_depend", metadata,
                     Column('group_id', Integer, ForeignKey('job_group.id')),
                     Column('job1', Integer, ForeignKey('job.id'), primary_key=True),
                     Column('job2', Integer, ForeignKey('job.id'), primary_key=True))

    def register_router(self):
        """
        Register router of job service
        """

        @self.route("/data/all_jobs", methods=["GET", "POST"])
        def all_jobs():
            try:
                jds = self.engine.execute(jd_t.select()).fetchall()
                job_depends = {}
                for jd in jds:
                    job1 = jd['job1']
                    job2 = jd['job2']
                    if job1 in job_depends:
                        job_depends[job1].append(job2)
                    else:
                        job_depends[job1] = [job2]
                rows = self.engine.execute(job_t.select()).fetchall()
                result = []
                for row in rows:
                    item = dict(row.items())
                    item["depends"] = job_depends.get(row["id"])
                    result.append(item)
                return json.dumps(result)
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/update_jobs", methods=["GET", "POST"])
        def update_jobs():
            # obtain changed jobs
            items = json.loads(request.form["json"])
            # vertify items
            for item in items:
                if item.get("id") == '':
                    item["id"] = None
                if item.get("worker_gid") == '':
                    item["worker_gid"] = None
                trigger = item.get("trigger")
                if not item.get("group_id") or not item.get("name") or not trigger or not\
                item.get("running_timeout"):
                    return RESPONSE_EMPTY_FIELD
                if not re.match("^((\d{1,4}|\*)\s){4}(\d{1,4}|\*)$", item.get("trigger")):
                    return FailResponse("Trigger illegal").to_json()
            # save into the db
            try:
                session = SessionBuilder()
                for item in items:
                    if "addFlag" in item:
                        session.execute(job_t.insert(), item)
                    else:
                        where_ = job_t.c.id==item.pop("id")
                        session.execute(job_t.update().where(where_), item)
                session.commit()
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                session.rollback()
                return FailResponse(str(e)).to_json()
            finally:
                session.close()

        @self.route("/data/delete_jobs", methods=["GET", "POST"])
        def delete_jobs():
            ids = request.form["id"]
            where_ = job_t.c.id.in_(ids.split(","))
            try:
                self.engine.execute(job_t.delete().where(where_))
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/all_jds", methods=["GET", "POST"])
        def all_job_depends():
            try:
                jds = self.engine.execute(jd_t.select()).fetchall()
                return row2json(jds)
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/add_jds", methods=["GET", "POST"])
        def add_jds():
            # obtain changed job depends
            items = json.loads(request.form["json"])
            # vertify items
            for item in items:
                if "group_id" not in item or "job1" not in item or "job2" not in item:
                    return RESPONSE_EMPTY_FIELD
            # save into the db
            try:
                session = SessionBuilder()
                for item in items:
                    session.execute(jd_t.insert(), item)
                session.commit()
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                session.rollback()
                return FailResponse(str(e)).to_json()
            finally:
                session.close()

        @self.route("/data/delete_jds", methods=["GET", "POST"])
        def delete_jds():
            items = json.loads(request.form["json"])
            try:
                session = SessionBuilder()
                for item in items:
                    where_ = and_(jd_t.c.job1 == item["job1"], jd_t.c.job2 == item["job2"])
                    session.execute(jd_t.delete().where(where_))
                session.commit()
                return RESPONSE_SUCCESS
            except Exception as e:
                session.rollback()
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()
            finally:
                session.close()

        @self.route("/data/all_jgs", methods=["GET", "POST"])
        def all_groups():
            try:
                rows = self.engine.execute(jg_t.select()).fetchall()
                return row2json(rows)
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/update_jgs", methods=["GET", "POST"])
        def update_jgs():
            # obtain job groups
            items = json.loads(request.form["json"])
            # veritify the input data
            for item in items:
                if item.get("id") == '':
                    item["id"] = None
                if item.get("first_job_id") == '':
                    item["first_job_id"] = None
                if not item.get("name"):
                    return RESPONSE_EMPTY_FIELD
            try:
                session = SessionBuilder()
                for item in items:
                    if "addFlag" in item:
                        session.execute(jg_t.insert(), item)
                    else:
                        where_ = jg_t.c.id==item.pop("id")
                        session.execute(jg_t.update().where(where_), item)
                session.commit()
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                session.rollback()
                return FailResponse(str(e)).to_json()
            finally:
                session.close()

        @self.route("/data/delete_jgs", methods=["GET", "POST"])
        def delete_jgs():
            ids = request.form["id"]
            try:
                session = SessionBuilder()
                where_ = job_t.c.group_id.in_(ids.split(","))
                session.execute(job_t.delete().where())
                where_ = jg_t.c.id.in_(ids.split(","))
                session.execute(jg_t.delete().where(where_))
                session.commit()
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.warn(format_exc())
                session.rollback()
                return FailResponse(str(e)).to_json()
            finally:
                session.close()

        @self.route("/data/alive_job_groups", methods=["GET", "POST"])
        def alive_job_groups():
            try:
                resp = ServerProxy(self.rpc_url).get_alive_job_groups()
                if resp["code"] == 0:
                    return json.dumps(resp["content"])
                else:
                    return FailResponse(resp["content"])
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/alive_task_groups", methods=["GET", "POST"])
        def alive_task_groups():
            try:
                resp = ServerProxy(self.rpc_url).get_alive_task_groups()
                if resp["code"] == 0:
                    return json.dumps(resp["content"])
                else:
                    return FailResponse(resp["content"])
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/job/apply_group", methods=["GET", "POST"])
        def apply_job_group():
            try:
                gid = int(request.args["gid"])
                resp = ServerProxy(self.rpc_url).apply_job_group(gid)
                if resp["code"] == 0:
                    return RESPONSE_SUCCESS
                else:
                    return FailResponse(resp["content"]).to_json()
            except Exception as e:
                self.logger.warn(format_exc())
                return FailResponse(str(e)).to_json()

        @self.route("/data/uploadscript", methods=["GET", "POST"])
        def upload_job_script():
            try:
                job_id = request.form["jid"]
                f = request.files["file"]
                filepath = os.path.join(self.local_script_path, job_id)
                f.save(filepath)
                with open(filepath, "rb") as f:
                    self.fs_client.upload(f, self.fs_script_path, job_id)
                os.remove(filepath)
                return RESPONSE_SUCCESS
            except Exception as e:
                self.logger.error(format_exc())
                return FailResponse(str(e)).to_json()

