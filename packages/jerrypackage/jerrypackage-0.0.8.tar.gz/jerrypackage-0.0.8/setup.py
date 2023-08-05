# coding: utf-8

from setuptools import setup

setup(
    name='jerrypackage',
    version='0.0.8',
    author='jerrychy',
    author_email='jerrychen@ustc.edu',
    url='https://www.zhihu.com/people/jerrychen-57/activities',
    description='Tools for daily use',
    packages=['jerrypackage.omtv', 'jerrypackage.tools', 'jerrypackage.xzb'],
    install_requires=[
        'requests>=2.18.4',
        'beautifulsoup4>=4.6.0'
	],
    entry_points={
        'console_scripts': [

        ]
    }
)