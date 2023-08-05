#! /usr/bin/env python

try:
    from setuptools import setup
    is_setuptools = True
except ImportError:
    from distutils.core import setup
    is_setuptools = False

kw = {}
if is_setuptools:
    kw['python_requires'] = '>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'
    kw['install_requires'] = ['m_lib>=3.1', 'm_lib.defenc>=1.0']

setup(name = "m_lib.full",
    version = "1.0.1",
    description = "m_lib full meta-package",
    long_description = "Broytman Library for Python, Copyright (C) 1996-2018 PhiloSoft Design",
    author = "Oleg Broytman",
    author_email = "phd@phdru.name",
    url = "http://phdru.name/Software/Python/#m_lib",
    license = "GPL",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms = "Any",
    packages = ["m_lib"],
    namespace_packages = ["m_lib"],
    **kw
)
