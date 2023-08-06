# -*- coding: utf-8 -*-
"""setup.py."""

from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'pyOpenSSL==17.5.0',
    'cryptography>=1.5.2'
]

VERSION = '0.0.7'

LONG_DESCRIPTION = 'cryptokit is a cryptography kit base on pyca Cryptography.'

setup(
    name='cryptokit',
    version=VERSION,
    description='cryptokit is a cryptography kit base on pyca Cryptography.',
    long_description=LONG_DESCRIPTION,
    author='silence',
    author_email='istommao@gmail.com',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/istommao/cryptokit',
    keywords='cryptokit is a cryptography kit base on pyca Cryptography!'
)
