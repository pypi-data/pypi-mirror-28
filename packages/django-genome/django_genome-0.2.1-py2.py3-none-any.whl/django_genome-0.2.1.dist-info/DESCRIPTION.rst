=============================
Django Genome
=============================

.. image:: https://badge.fury.io/py/django-genome.svg
    :target: https://badge.fury.io/py/django-genome

.. image:: https://travis-ci.org/chopdgd/django-genome.svg?branch=develop
    :target: https://travis-ci.org/chopdgd/django-genome

.. image:: https://codecov.io/gh/chopdgd/django-genome/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/chopdgd/django-genome

.. image:: https://pyup.io/repos/github/chopdgd/django-genome/shield.svg
    :target: https://pyup.io/repos/github/chopdgd/django-genome/
    :alt: Updates

.. image:: https://pyup.io/repos/github/chopdgd/django-genome/python-3-shield.svg
    :target: https://pyup.io/repos/github/chopdgd/django-genome/
    :alt: Python 3

Django app for syncing and storing human genome reference data

Documentation
-------------

The full documentation is at https://django-genome.readthedocs.io.

Quickstart
----------

Install Django Genome::

    pip install django-genome

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'genome',
        ...
    )

Add Django Genome's URL patterns:

.. code-block:: python

    from genome import urls as genome_urls


    urlpatterns = [
        ...
        url(r'^', include(genome_urls, namespace='genome')),
        ...
    ]

Initial sync for genome models::

    python manage.py genome_sync

Features
--------

* Includes models for Genome, Chromosome, CytoBand, Gene, Transcript, and Exons
* Syncs data for hg18, hg19, hg38 from HGNC and UCSC

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2017-12-30)
++++++++++++++++++

* First release on PyPI.
* Initial models and REST API
* Syncs data from HGNC and UCSC to build database

0.2.0 (2018-01-5)
++++++++++++++++++

* Improved REST API Filters
* made Chromosomes and Gene Symbols save as uppercase to maintain consistency


