[![Build
Status](<https://travis-ci.org/DaveTCode/communardo-metadata-python-lib.svg?branch=master>)](<https://travis-ci.org/DaveTCode/communardo-metadata-python-lib>)
[![PyPI
version](<https://badge.fury.io/py/communardo-metadata.svg>)](<https://badge.fury.io/py/communardo-metadata>)

\# Communardo Metadata Python Library

This is a simple wrapper around the REST API which the Communardo
Metadata plugin for Confluence provides.

\#\# Installation

Install from pypi use: \~\~\~\~ pip install communardo-metadata \~\~\~\~

\#\# Usage

`` `python from communardo.metadata.client import MetadataClient with MetadataClient("https://server:port/contextpath", ("user", "pass")) as client:     metadata_results = client.search(cql="ID=1") ``\`

\#\# Development and Deployment

See the [Contribution guidelines for this project](CONTRIBUTING.md) for
details on how to make changes to this library.


