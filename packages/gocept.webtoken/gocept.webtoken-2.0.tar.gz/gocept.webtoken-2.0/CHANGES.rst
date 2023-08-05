gocept.webtoken
===============

2.0 (2018-01-08)
----------------

- Drop support for Python 3.3 but add it for 3.6.

- Make `setup.py` compatible with newer `setuptools` versions by no longer
  using absolute paths.


1.2.1 (2015-10-08)
------------------

- Fix `extract_token` to accept any ``collections.Mapping`` derived object.


1.2 (2015-10-08)
----------------

- Added helper functions to create a Bearer Authorization header and extract
  a token from it.

- Officially support Python 3.5.


1.1 (2015-10-01)
----------------

- Shortened imports for `CryptographicKeys`, `create_web_token` and
  `decode_web_token`, which are now importable directly from `gocept.webtoken`.

- Added documentation.


1.0 (2015-10-01)
----------------

* Add support for Python 3.3 and 3.4.

* Initial release, extracted from internally used package.
