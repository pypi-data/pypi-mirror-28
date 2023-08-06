=======
NiPyApi
=======

Nifi-Python-Api: A convenient Python wrapper for the Apache NiFi Rest API

.. image:: https://img.shields.io/pypi/v/nipyapi.svg
        :target: https://pypi.python.org/pypi/nipyapi
        :alt: Release Status

.. image:: https://img.shields.io/travis/Chaffelson/nipyapi.svg
        :target: https://travis-ci.org/Chaffelson/nipyapi
        :alt: Build Status

.. image:: https://readthedocs.org/projects/nipyapi/badge/?version=latest
        :target: https://nipyapi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Chaffelson/nipyapi/shield.svg
     :target: https://pyup.io/repos/github/Chaffelson/nipyapi/
     :alt: Python Updates

.. image:: https://coveralls.io/repos/github/Chaffelson/nipyapi/badge.svg?branch=master
    :target: https://coveralls.io/github/Chaffelson/nipyapi?branch=master&service=github
    :alt: test coverage

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License


Features
--------

| This package provides pythonic calls for common NiFi tasks and CICD/SDLC integrations - you might call it Flow Development LifeCycle
| These are implemented by replicating the action of the same task in the GUI and surfacing the underlying NiFi Data structures and calls wherever possible, to retain UX parallelism for the user

Functionality Highlights:
 - Full native Python rest client for NiFi and NiFi-Registry
 - CRUD wrappers for common task areas like Processor Groups, Processors, Templates, Registry Clients, Registry Buckets, Registry Flows, etc.
 - Convenience functions for inventory tasks, such as recursively retrieving the entire canvas, or a flat list of all Process Groups
 - Docker Compose configurations for testing and deployment
 - Limited support for scheduling components
 - A scripted deployment of an interactive environment for testing and demonstration purposes

Coming soon:
 - Secured environment support is not currently implemented, but it is planned to be done very soon
 - Support for complex scheduling requests, such as stopping a large flow and waiting for all Processors to be halted
 - Support for edge cases during Versioning changes, such as Reverting a flow containing live data

Usage
-----
The easiest way to install NiPyApi is with pip::

    # in bash
    pip install nipyapi

Then import a module and execute tasks::

    # in python
    from nipyapi import config
    config.nifi_config.host = 'http://localhost:8080/nifi-api'
    from nipyapi.canvas import get_root_pg_id
    get_root_pg_id()
    >'4d5dcf9a-015e-1000-097e-e505ed0f7fd2'

You can also use the demo to create an interactive console showing a few of the features::

    # in python
    from nipyapi import config
    config.nifi_config.host = 'http://localhost:8080/nifi-api'
    config.registry_config.host = 'http://localhost:18080/nifi-registry-api'
    from nipyapi.demo.console import *

You can also pull the repository from Github and use or contribute to the latest features.
Please check out the `Contribution Guide <https://github.com/Chaffelson/nipyapi/blob/master/docs/contributing.rst>`_ for more info.

Background
----------

| For more information on Apache NiFi, please visit `https://nifi.apache.org <https://nifi.apache.org>`_
| For Documentation on this package please visit `https://nipyapi.readthedocs.io. <https://nipyapi.readthedocs.io/en/latest>`_


Version Support
---------------

| Currently we are testing against NiFi version 1.2 - 1.5, and NiFi-Registry version 0.1.0
| If you find a version compatibility problem please raise an `issue <https://github.com/Chaffelson/nipyapi/issues>`_

Requirements
------------

Python 2.7 or 3.6 supported, though other versions may work


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Inspired by the equivalent Java client maintained over at
`hermannpencole/nifi-config <https://github.com/hermannpencole/nifi-config>`_

The swagger 2.0 compliant client auto-generated using the
`Swagger Codegen <https://github.com/swagger-api/swagger-codegen>`_ project,
and then cleaned / bugfixed by the authors

Props to the NiFi-dev and NiFi-user mailing list members over at Apache for all the assistance and kindnesses.


=======
History
=======

0.7.0 (2018-01-30)
------------------

* Updated project to support NiFi-1.5.0 and NiFi-Registry-0.1.0
* Merged api clients into main codebase, deprecated external client requirement
* Created centralised project configuration and test configuration
* Updated automated test environment to consistent docker for local and Travis
* Removed procedurally generated boilerplate stub tests to improve readability
* Moved pytest fixtures into conftest and expanded dramatically
* Added limited support for processor and process group scheduling
* Added support for all common Nifi-Registry calls
* Added a demo package to provide an interactive test and demo console
* Significant readme, contribution, and other documentation refresh
* Expanded CRUD support for most processor, process group and related tasks


0.6.1 (2018-01-04)
------------------

* Added requested functions to find and list Processors on the canvas
* Fixed list all process groups to include the root special case properly


0.6.0 (2017-12-31)
------------------

* Refactored many functions to use native NiFi datatypes instead of generics
* Standardised several call names for consistency
* Updated examples
* Created additional tests and enhanced existing to capture several exceptions


0.5.1 (2017-12-07)
------------------

* Added template import/export with working xml parsing and tests
* Added a ton of testing and validation steps
* Cleared many todos out of code by either implementing or moving to todo doc


0.5.0 (2017-12-06)
------------------

* migrated swagger_client to separate repo to allow independent versions
* refactored wrapper Classes to simpler functions instead
* cleaned up documentation and project administrivia to support the split

0.4.0 (2017-10-29)
------------------

* Added wrapper functions for many common Template commands (templates.py)
* Added new functions for common Process Groups commands (canvas.py)
* Significant test framework enhancements for wrapper functions
* Many coding style cleanups in preparation for filling out test suite
* Added linting
* Cleaned up docs layout and placement within project
* Integrated with TravisCI
* Dropped Python2.6 testing (wasn't listed as supported anyway)
* Updated examples and Readme to be more informative

0.3.2 (2017-09-04)
------------------

* Fixed bug where tox failing locally due to coveralls expecting travis
* Fixed bug where TravisCI failing due to incorrectly set install requirements
* Fixed bug where swagger_client not importing as expected


0.3.1 (2017-09-04)
------------------

* Fixed imports and requirements for wheel install from PyPi

0.3.0 (2017-09-04)
------------------

* Created basic wrapper structure for future development
* Added simple usage functions to complete todo task
* Added devnotes, updated usage, and various sundry other documentation cleanups
* Split tests into subfolders for better management and clarity
* Added Coveralls and License Badge
* Removed broken venv that ended up in project directory, added similar to ignore file
* Changed default URL in the configuration to default docker url and port on localhost

0.2.1 (2017-08-26)
------------------

* Fixed up removal of leftover swagger client dependencies

0.2.0 (2017-08-25)
------------------

* Merge the nifi swagger client into this repo as a sub package
    * Restructured tests into package subfolders
    * Consolidate package configuration
    * Setup package import structure
    * Updated usage instructions
    * Integrate documentation

0.1.2 (2017-08-24)
------------------

* Created basic integration with nifi-python-swagger-client

0.1.1 (2017-08-24)
------------------

* Cleaned up base project and integrations ready for code migration

0.1.0 (2017-08-24)
------------------

* First release on PyPI.


