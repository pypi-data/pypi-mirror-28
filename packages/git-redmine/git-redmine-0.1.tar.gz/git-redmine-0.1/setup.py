#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='git-redmine',
    version='0.1',
    py_modules=['git_redmine'],
    install_requires=[
        'Click',
        'python-redmine',
        'GitPython',
    ],
    entry_points={
        'console_scripts': ['git-redmine=git_redmine:redmine'],
    }
)
