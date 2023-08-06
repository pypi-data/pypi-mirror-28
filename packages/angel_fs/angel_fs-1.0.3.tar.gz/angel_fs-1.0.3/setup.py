#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2018-01-10
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93


from setuptools import setup, find_packages
import sys
import os

ETC_PATH = "/etc/angel/fs/"

setup(
    name="angel_fs",
    version="1.0.3",
    author="Lafite93",
    author_email="2273337844@qq.com",
    description="The filesystem of a distribute job scheduler named 'angel'",
    license="Apache",
    keywords="angel filesystem",
    url="https://pypi.python.org/pypi/angel_fs",
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        (ETC_PATH, ['etc/fs.conf', 'etc/logger.conf'])
    ],
    scripts=["scripts/fs_daemon"],
    install_requires=[
        "pyftpdlib",
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
            "start_fs = angel_fs.filesystem:serve_forever"
        ]
    }
)
