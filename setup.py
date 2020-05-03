# -*- coding: utf-8 -*-

import ast
from io import open
import re
from setuptools import setup, find_packages

'''
How to build and upload this package to PyPi
    python setup.py sdist
    python setup.py bdist_wheel --universal
    twine upload dist/*

How to build and upload this package to Local site:
    python setup.py install
'''

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("robotframework_sqlcli/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )


def open_file(filename):
    """Open and read the file *filename*."""
    with open(filename, 'r+', encoding='utf-8') as f:
        return f.read()


readme = open_file("README.md")

setup(
    name='robotframework-sqlcli',
    version=version,
    description='SQL Command tool, use JDBC, jaydebeapi',
    long_description=readme,
    keywords='robotframework sqlcli',
    platforms='any',
    install_requires=['robotslacker-sqlcli',],

    author='RobotSlacker',
    author_email='184902652@qq.com',
    url='https://github.com/robotslacker/robotframework-sqlcli',

    packages=find_packages(),
    package_data={"robotframework-sqlcli": []},
)
