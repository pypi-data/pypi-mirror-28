#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from pip.req import parse_requirements
from pip.download import PipSession
from backup2s3 import __version__

try:
    from setuptools import setup, find_packages
    from setuptools.command.build_py import build_py as BuildPy
    from setuptools.command.install_lib import install_lib as InstallLib
    from setuptools.command.install_scripts import install_scripts as InstallScripts
except ImportError:
    print("Backup2s3 now needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def read_requirements():
    '''parses requirements from requirements.txt'''
    reqs_path = os.path.join(__location__, 'requirements.txt')
    install_reqs = parse_requirements(reqs_path, session=PipSession())
    reqs = [str(ir.req) for ir in install_reqs]
    return reqs


setup(
    name="backup2s3",
    version=__version__,
    packages=["backup2s3"],
    description="Backup files and mysql to AWS S3",
    license="GPLv3",
    author="Nazar Suryev",
    author_email="wavedocs@gmail.com",
    url="https://github.com/wavedocs/backup2s3",
    download_url="https://github.com/wavedocs/backup2s3/archive/0.1.tar.gz",
    keywords=["backup", "s3", "mysql"],
    long_description=open("README.md").read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    install_requires=read_requirements(),
    scripts=['bin/backup2s3'],
    data_files=[('/etc/', ['backup2s3-sample.yml'])]
)
