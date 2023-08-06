# coding: utf-8

"""
    stylelens-s3


"""


import sys
from setuptools import setup, find_packages

NAME = "stylelens-s3"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["boto3"]

setup(
    name=NAME,
    version=VERSION,
    description="stylelens-s3",
    author_email="master@bluehack.net",
    url="",
    keywords=["BlueLens", "stylelens-s3"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)
