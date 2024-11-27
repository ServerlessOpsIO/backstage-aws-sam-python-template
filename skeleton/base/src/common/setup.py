#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='common',
    version='0.0.1',
    description='${{ values.component_name }} common code',
    author='NBCUniversal',
    license='Apache License 2.0',
    packages=find_packages(exclude=['tests.*', 'tests']),
    keywords="${{ values.component_name }} service",
    python_requires='>=${{ values.python_version }}',
    include_package_data=True,
    install_requires=[
        'aws_lambda_powertools',
        'boto3'
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Other Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: ${{ values.python_version }}',
    ]
)

