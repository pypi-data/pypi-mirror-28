#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='SimpleQuestions',
    version='1.0.1',
    description='Add a function to ask Yes/No questions',
    author='Rémy Jacquin',
    author_email='remy@remyj.fr',
    url='https://gitlab.com/remyj38/simplequestions',
    packages=['simplequestions'],
    license='GPLv3',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    keywords='yes no questions'
)
