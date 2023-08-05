#! /usr/bin/env python

from __future__ import absolute_import

import sys
import platform

import oa
import distutils.core

requirements = [
    "dill==0.2.5",
    "future==0.15.2",
    "raven==5.13.0",
    "pyzor==1.0.0",
    "Pillow==4.0.0",
    "pygeoip==0.3.2",
    "python-dateutil==2.6.0",
    "langdetect==1.0.6",
    "PyPDF2==1.25.1",
    "pyspf==2.0.12t",
    "spoon==1.0.1",
    "dkimpy==0.5.6",
]

if "pypy" in platform.python_implementation().lower():
    if sys.version_info.major == 3:
        requirements.extend([
            "ipaddress==1.0.16",
        ])
        requirements.extend([
            "dnspython3==1.12.0",
            "py3dns==3.1.0",
        ])
    elif sys.version_info.major == 2:
        requirements.extend([
            "ipaddress==1.0.16",
            "dnspython==1.12.0",
            "pydns==2.3.6",
            "ipaddr==2.1.11",
        ])
else:
    if sys.version_info.major == 3:
        requirements.extend([
            "dnspython3==1.12.0",
            "py3dns==3.1.0",
        ])
        if sys.version_info.minor == 2:
            requirements.extend([
                "ipaddress==1.0.16",
            ])
            requirements.extend([
                "dnspython3==1.12.0",
                "py3dns==3.1.0",
            ])
    elif sys.version_info.major == 2:
        requirements.extend([
            "ipaddress==1.0.16",
            "dnspython==1.12.0",
            "pydns==2.3.6",
            "ipaddr==2.1.11",
        ])

distutils.core.setup(
    name='OrangeAssassin',
    version=oa.__version__,
    scripts=[
        'scripts/match.py',
        'scripts/oad.py',
        'scripts/compile.py'
    ],
    packages=[
        'oa',
        'oa.rules',
        'oa.plugins',
        'oa.protocol',
    ],
    install_requires=requirements,
)
