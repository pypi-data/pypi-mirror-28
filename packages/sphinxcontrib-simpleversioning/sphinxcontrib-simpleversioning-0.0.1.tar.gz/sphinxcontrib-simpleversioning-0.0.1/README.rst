==============================
sphinxcontrib-simpleversioning
==============================

Sphinx extension that allows adding version selection to docs.

* Python 2.7, 3.3, 3.4, and 3.5 supported

This is based on, but is a vastly simplified version of sphinxcontrib.versioning_ intended for building and publishing
documentation with automation/continuous integration tools.

See the sphinxcontrib.versioning_ documentation if you need more features or would like to understand the differences.

.. _sphinxcontrib.versioning: https://robpol86.github.io/sphinxcontrib-versioning/

📖 Full documentation: https://sphinxconfig-simpleversioning.readthedocs.io/

Quickstart
==========

Install:

.. code:: console

    pip install sphinxcontrib-versioning

Usage (in Sphinx ``conf.py``):

.. code:: python

    extensions.append('sphinxcontrib.simpleversioning')
    simpleversioning_versions = [
        'master',
        {'id': 'dev', 'name': 'latest'},
    ]

.. changelog-section-start

Changelog
=========

This project adheres to `Semantic Versioning <http://semver.org/>`_.

0.0.1 - 2017-01-17
------------------

* Initial development/testing version.

.. changelog-section-end
