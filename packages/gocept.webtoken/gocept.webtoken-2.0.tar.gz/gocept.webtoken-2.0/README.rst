================================
The gocept.webtoken distribution
================================

This library helps you using JWT tokens with the Zope Component Architecture
(ZCA).

This package is compatible with Python version 2.7, 3.4, 3.5 and 3.6.

Copyright (c) 2015-2018 gocept gmbh & co kg

All Rights Reserved.

This software is subject to the provisions of the Zope Public License,
Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE.

Installation
============

This package requires ``cryptography``, which needs some install attention.
Please refer to its `install documentation`_ for further information.


.. _`install documentation`: https://cryptography.io/en/latest/installation/

.. contents::

Usage
=====

The ``CryptographicKey`` utility
--------------------------------

``gocept.webtoken`` uses a global utility of the class
``gocept.webtoken.CryptographicKeys``, which provides cryptographic keys for
different purposes. It loads a set of public and private keys from disk. It
takes the filesystem path to your key files and a list of key names::

    >>> import gocept.webtoken
    >>> import pkg_resources
    >>> path_to_keys = pkg_resources.resource_filename(
    ...     'gocept.webtoken', 'testing/keys')
    >>> keys = gocept.webtoken.CryptographicKeys(
    ...     path_to_keys, ['key1'])

For each of the names, a private key file of the same name and a public key
file (with a .pub suffix) must reside inside the keys_dir.

The utility needs to be registered at the ZCA, either via a zcml file or via::

    >>> import zope.component
    >>> zope.component.provideUtility(keys)


Creating a token
----------------

Create a signed web token with the function ``create_web_token``. You will need
the private key name, which was registered at the CryptographycKey utility. It
is referenced by its name and the suffix ``-private``::

    >>> expires_in = 300  # The token is valid for 300 seconds
    >>> payload = {'your': 'data'}
    >>> result = gocept.webtoken.create_web_token(
    ...     'key1-private', 'issuer', 'subject', expires_in, payload)
    >>> sorted(result.keys())
    ['data', 'token']

The token is available under the key ``token``, while the data encoded in the
token is placed under the key ``data``.


Creating a Bearer Authorization header
--------------------------------------

You can create an `Bearer Authorization header`_ either from a token_dict as
returned by create_web_token or from a token directly::

    >>> gocept.webtoken.create_authorization_header(b'<TOKEN>')
    ('Authorization', 'Bearer <TOKEN>')

.. _`Bearer Authorization header`: https://tools.ietf.org/html/rfc6750#section-2.1

Extracting a token from a Bearer Authorization header
-----------------------------------------------------

Extract the token from a dict containing the headers of you request or from the
value of the HTTP Authorization header itself::

    >>> request_headers = dict(Authorization='Bearer <TOKEN>')
    >>> b'<TOKEN>' == gocept.webtoken.extract_token(request_headers)
    True


Decoding a token
----------------

Decode a signed web token with the function ``decode_web_token``. You will need
the public key name, which was registered at the CryptographycKey utility. It
is referenced by its name and the suffix ``-public``::

    >>> result = gocept.webtoken.decode_web_token(
    ...     result['token'], 'key1-public', 'subject')

Note that the subject must match the subject given when the token was created.

The result contains all data encoded in the token. You can find the payload
under the key ``data``::

    >>> {'your': 'data'} == result['data']
    True

