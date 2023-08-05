[![Build Status](https://travis-ci.org/DaveTCode/communardo-metadata-python-lib.svg?branch=master)](https://travis-ci.org/DaveTCode/communardo-metadata-python-lib)

# Communardo Metadata Python Library

This is a simple wrapper around the REST API which the Communardo Metadata plugin 
for Confluence provides.

## Installation

Install from pypi using
~~~~
pip install comala-workflows
~~~~

## Usage

```python
from communardo.metadata.client import MetadataClient
client = MetadataClient("https://server:port/contextpath", ("user", "pass"))
metadata_results = client.search(cql="ID=1")
```

## Development and Deployment

See the [Contribution guidelines for this project](CONTRIBUTING.md) for details on how to make changes to this library.