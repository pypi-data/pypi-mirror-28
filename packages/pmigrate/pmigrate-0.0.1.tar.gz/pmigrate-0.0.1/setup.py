#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='pmigrate',
    version='0.0.1',
    author='Brent Tubbs',
    author_email='brent.tubbs@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'psycopg2',
        'pyyaml',
    ],
    url='https://github.com/btubbs/pmigrate',
    description="A Postgres-specific tool for versioning your DB schema.",
    # long_description=open('README.rst').read(),
    entry_points={
        'console_scripts': [
            'pmigrate = pmigrate.cli:main',
        ]
    },
)
