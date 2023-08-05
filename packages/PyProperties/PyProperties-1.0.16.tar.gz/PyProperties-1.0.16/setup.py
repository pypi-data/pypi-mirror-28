# coding=utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='PyProperties',
    version='1.0.16',
    description='Python library operating with java properties file',
    long_description=long_description,
    url='https://github.com/seelikes/PyProperties',
    author='seelikes',
    author_email='seelikes@163.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='py properties',
    packages=find_packages(exclude=['test']),
    data_files=[('test_resources', ['test/resources/test.properties'])],
)
