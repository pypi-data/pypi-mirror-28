"""Setup file.
"""
from __future__ import absolute_import, print_function, unicode_literals

from os import path

from setuptools import setup, find_packages

README_PATH = path.join(path.dirname(path.abspath(__file__)), 'README.md')
VERSION_PATH = path.join(path.dirname(path.abspath(__file__)), 'version.txt')

with open(VERSION_PATH) as version_file:
    VERSION = version_file.read().strip()

try:
    import m2r
    LONG_DESCRIPTION = m2r.parse_from_file(README_PATH)
except (ImportError, IOError, FileNotFoundError):
    # m2r not installed or file does not exist
    LONG_DESCRIPTION = ''

setup(
    name='slack-releaser',
    version=VERSION,
    description="A zest.releaser plugin for posting changelogs to Slack",
    author="Pebble",
    author_email="sysadmin@mypebble.co.uk",
    install_requires=[
        'zest.releaser', 'requests',
    ],
    long_description=LONG_DESCRIPTION,
    license='MIT',
    url="https://github.com/mypebble/slack-releaser",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
