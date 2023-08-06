httpsig-pure-hmac
=================

.. image:: https://travis-ci.org/alexanderlukanin13/httpsig-pure-hmac.svg?branch=master
    :target: https://travis-ci.org/alexanderlukanin13/httpsig-pure-hmac

Fork of Adam Knight's httpsig_, providing the same functionality, except that:

* RSA is not supported.

* PyCrypto is not required.

This package is intended as a lightweight option for HMAC-only clients.

.. _httpsig: https://pypi.python.org/pypi/httpsig

Requirements
------------

* Python 2.7, 3.3+

* six

Usage
-----

.. code:: python

    import httpsig_pure_python as httpsig

See `original package`_ for more info.

.. _`original package`: https://pypi.python.org/pypi/httpsig
