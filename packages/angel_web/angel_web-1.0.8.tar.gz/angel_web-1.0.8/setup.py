#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2018-01-10
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93


from setuptools import setup, find_packages
import sys
import os

ETC_PATH = "/etc/angel/web/"

if "install" in sys.argv:
    if not os.path.isdir(ETC_PATH):
        os.makedirs(ETC_PATH)
    web_config_file = os.path.join(ETC_PATH, "web.conf")
    log_config_file = os.path.join(ETC_PATH, "logger.conf")
    if not os.path.isfile(web_config_file):
        with open(os.path.join(ETC_PATH, "web.conf"), "w") as fw:
            with open("etc/web.conf", "r") as fr:
                fw.write(fr.read())
    if not os.path.isfile(log_config_file):
        with open(os.path.join(ETC_PATH, "logger.conf"), "w") as fw:
            with open("etc/logger.conf", "r") as fr:
                fw.write(fr.read())

setup(
    name="angel_web",
    version="1.0.8",
    author="Lafite93",
    author_email="2273337844@qq.com",
    description="The admin web dashboard of a distribute job scheduler named 'angel'",
    license="Apache",
    keywords="angel admin web dashboard",
    url="https://pypi.python.org/pypi/angel_web",
    packages=find_packages(),
    include_package_data=True,
    scripts=["scripts/angel_web.py"],
    install_requires=[
        "flask",
        "sqlalchemy",
        "flask_socketio",
        "configparser",
        "daemonpy3"
    ],
    zip_safe=False,
    platforms=["Linux", "Unix"],
    classifiers = [
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        "console_scripts":[
            "start_angelweb = angel_web.app:serve_forever"
        ]
    }
)
