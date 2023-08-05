"""Wrapper around JWT tokens and the Zope Component Architecture (ZCA)."""

from setuptools import setup, find_packages

setup(
    name='gocept.webtoken',
    version='2.0',

    install_requires=[
        'cryptography',
        'pyjwt',
        'setuptools',
        'zope.interface',
        'zope.component',
    ],

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://bitbucket.org/gocept/gocept.webtoken',
    keywords='jwt token webtoken ZCA',
    classifiers="""\
Development Status :: 4 - Beta
Intended Audience :: Developers
Natural Language :: English
Operating System :: OS Independent
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Security
Topic :: Security :: Cryptography
Topic :: Software Development
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
License :: OSI Approved
License :: OSI Approved :: Zope Public License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation
Programming Language :: Python :: Implementation :: CPython
"""[:-1].split('\n'),
    description=__doc__.strip(),
    long_description='\n\n'.join(open(name).read() for name in (
        'README.rst',
        'CHANGES.rst',
    )),

    namespace_packages=['gocept'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
