import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django_configdir",
    version = "0.1.8",
    author = "Seb Potter",
    author_email = "seb@woome.com",
    description = ("A utility to create per-user, per-host configuration "
        "files for Django."),
    license = "GPLv2",
    keywords = "django configuration instance utility user",
    url = "http://github.com/woome/django_configdir",
    packages=['configdir', 'configdir.management', 'configdir.management.commands'],
    requires=['django'],
    entry_points = {
        'console_scripts': [
            'django_confighelper = configdir.django_confighelper:main',
            'django-confighelper = configdir.django_confighelper:main',
            ]
    },
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Framework :: Django",
    ],
)
