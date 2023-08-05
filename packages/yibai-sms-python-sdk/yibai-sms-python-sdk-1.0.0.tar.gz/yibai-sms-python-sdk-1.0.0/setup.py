# -*- coding:utf-8 -*-
# filename:setup

__author__ = 'yibai'
from setuptools import setup, find_packages

setup(
    name='yibai-sms-python-sdk',
    version='1.0.0',
    keywords=('yibai', 'sms', 'sdk'),
    description='yibai python sdk',
    license='MIT',
    install_requires=['requests>=2.9.1'],
    author='shomop',
    author_email='lanran@shomop.com',
    packages=find_packages(),
    platforms='any',
)
