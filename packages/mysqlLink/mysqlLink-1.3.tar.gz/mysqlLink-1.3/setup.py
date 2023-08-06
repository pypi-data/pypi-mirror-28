# -*- coding:utf-8 -*-
# Made by Azrael

from distutils.core import setup
from setuptools import setup

setup(
    name='mysqlLink',
    version='1.3',
    py_modules = ['mysqlLink'],
    author='Azrael',
    author_email='yinyuhang1996@gmail.com',
    maintainer='Azrael',
    license='None',
    platforms=["python3 or later"],
    url='https://github.com/DawnAzrael/MysqlTools.git',
    description=('a tool for linking mysql with python3.6, base on module pymysql'),
    long_description=open('README.rst').read(),
    install_requires=['pymysql',],
)
