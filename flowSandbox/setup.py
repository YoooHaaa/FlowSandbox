# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : setup.py
# Time       ：2020/8/19 14:17
# Author     ：Rodney Cheung
"""

import os

import setuptools


def find_version(file_name):
    with open(file_name, encoding='utf-8') as file_handle:
        lines = file_handle.readlines()
        latest_version = lines[0].strip(os.linesep).rstrip(']').lstrip('[')
        print("Tweezer:", latest_version)
        return latest_version


setuptools.setup(
    name='tweezer',
    version=find_version("./ChangeLog"),
    description='sandbox',
    long_description='dynamic sandbox',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=[
        'tweezer', 'tweezer.*', 'wisbec', 'wisbec.*'
    ]),
    install_requires=[
        'mitmproxy>=5.2',
        'keyboard>=0.13.5',
        'proxy.py==2.2.0',
        'sshtunnel',
        'pymysql',
        'colorlog',
        'jsonpickle',
        # 'frida==14.1.2',
        'requests',
        'DBUtils',
        'psutil'],
    package_data={
        '': ['installation_pkg/platform-tools_r30.0.4-linux.zip',
             'installation_pkg/platform-tools_r30.0.4-darwin.zip',
             'installation_pkg/platform-tools_r30.0.4-windows.zip',
             # 'installation_pkg/mock_location.apk',
             'installation_pkg/android-tool.apk',
             'config/*',

             # 'decrypt/*.jar',
             # 'rules/*.json',
             'persist/*',
             # 'persist/frida_core/*'
            'installation_pkg/mitmcert.cer'
            ]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tweezer = tweezer.main:main",
        ]
    },
    python_requires='>=3.7,<3.9',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    zip_safe=False)
