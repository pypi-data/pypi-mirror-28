[![Build
Status](<https://travis-ci.org/DaveTCode/comala-workflow-python-lib.svg?branch=master>)](<https://travis-ci.org/DaveTCode/comala-workflow-python-lib>)
[![PyPI
version](<https://badge.fury.io/py/comala-workflows.svg>)](<https://badge.fury.io/py/comala-workflows>)

\# Comala Workflow Python Library

This is a simple wrapper around the REST API which the Comala Workflow
plugin for Confluence provides.

\#\# Installation

To install from pypi use:

\~\~\~\~ pip install comala-workflows \~\~\~\~

\#\# Usage

`` `python from comala.workflows.client import ComalaWorkflowsClient with ComalaWorkflowsClient("https://server:port/contextpath", ("user", "pass")) as client:     status = client.status(page_id=1, expand=['state','states','approvals','actions','tasks']) ``\`

\#\# Development and Deployment

See the [Contribution guidelines for this project](CONTRIBUTING.md) for
details on how to make changes to this library.


