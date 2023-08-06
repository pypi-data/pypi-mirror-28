from setuptools import find_packages, setup
import re

from sys import version_info

class NotSupportedException(BaseException): pass

if version_info.major < 3:
    raise NotSupportedException("Only Python 3.x Supported")

setup(
    name='dyckviz',
    description='Visualization utilities for Dyck words using Young tableaux and combinatorial spider webs.',
    entry_points = { "console_scripts": ['dyckviz = dyckviz.dyckviz:main'] },
    version = '0.4.0',
    author='Orestis Melkonian, Konstantinos Kogkalidis',
    author_email='melkon.or@gmail.com, konstantinos@riseup.net',
    url='http://github.com/omelkonian/dyckviz',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    python_requires='>=3',
    install_requires=[
        'ansicolors==1.1.8',
        'graphviz==0.8.2',
        'numpy==1.14.0',
        'pdfrw==0.4',
    ],
)
