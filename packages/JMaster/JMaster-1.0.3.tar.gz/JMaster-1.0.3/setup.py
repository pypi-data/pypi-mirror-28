#!/usr/bin/env python
from os import path
from setuptools import setup

setup_requires = ['click', 'terminaltables', 'colorclass', 'requests', 'lxml', 'beautifulsoup4']
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name="JMaster",
    version="1.0.3",
    description="JMaster, contest parser and tester for CodeForces",
    long_description=long_description,
    author="palayutm",
    author_email="palayutm@gmail.com",
    url="https://github.com/palayutm/JMaster",
    license="GPL",
    py_modules=['JMaster'],
    entry_points={
        'console_scripts': ['JMaster=JMaster:main'],
    },
    install_requires=setup_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: SunOS/Solaris",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ]
)
