# coding: utf-8

"""
    stylelens-user

    Utility package for bl-db-user, bl-db-user-log (DB)

"""


import sys
from setuptools import setup, find_packages

NAME = "stylelens-user"
VERSION = "0.0.8"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["pymongo"]

setup(
    name=NAME,
    version=VERSION,
    description="stylelens-user",
    author_email="master@bluehack.net",
    url="",
    keywords=["Swagger", "stylelens-user"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)
