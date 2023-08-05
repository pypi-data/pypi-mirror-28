#!/usr/bin/env python
# vim:set ts=4 sts=4 sw=4 et:

from setuptools import setup

from km3learn import version

setup(
    name='km3learn',
    version=version,
    description='Machine Learning',
    url='http://git.km3net.de/km3learn/km3learn',
    author='Moritz Lotze',
    author_email='mlotze@km3net.de',
    license='BSD-3',
    packages=['km3learn', ],
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'imbalanced-learn',
        'matplotlib>=2',
        'km3pipe[full]'
    ]
)
