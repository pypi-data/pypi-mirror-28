#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2018-01-10
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93


from setuptools import setup, find_packages
import sys
import os

ETC_PATH = "/etc/angel/web/"

setup(
    name="angel_web",
    version="1.0.16",
    author="Lafite93",
    author_email="2273337844@qq.com",
    description="The admin web dashboard of a distribute job scheduler named 'angel'",
    license="Apache",
    keywords="angel admin web dashboard",
    url="https://pypi.python.org/pypi/angel_web",
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('/etc/angel/web', ['etc/web.conf', 'etc/logger.conf'])
    ],
    scripts=["scripts/aweb_daemon.py"],
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
            "start_aweb = angel_web.app:serve_forever"
        ]
    }
)
