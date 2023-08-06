|Build Status| |PyPI version|

Communardo Metadata Python Library
==================================

This is a simple wrapper around the REST API which the Communardo
Metadata plugin for Confluence provides.

Installation
------------

Install from pypi use: ~\ :sub:`~` pip install communardo-metadata
~\ :sub:`~`

Usage
-----

.. code:: python

    from communardo.metadata.client import MetadataClient
    with MetadataClient("https://server:port/contextpath", ("user", "pass")) as client:
        metadata_results = client.search(cql="ID=1")

Development and Deployment
--------------------------

See the `Contribution guidelines for this project <CONTRIBUTING.md>`__
for details on how to make changes to this library.

.. |Build Status| image:: https://travis-ci.org/DaveTCode/communardo-metadata-python-lib.svg?branch=master
   :target: https://travis-ci.org/DaveTCode/communardo-metadata-python-lib
.. |PyPI version| image:: https://badge.fury.io/py/communardo-metadata.svg
   :target: https://badge.fury.io/py/communardo-metadata


