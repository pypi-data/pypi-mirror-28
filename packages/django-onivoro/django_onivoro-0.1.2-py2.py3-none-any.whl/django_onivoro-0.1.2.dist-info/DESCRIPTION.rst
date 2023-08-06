=============================
Django Onivoro
=============================

.. image:: https://badge.fury.io/py/django-onivoro.svg
    :target: https://badge.fury.io/py/django-onivoro

.. image:: https://travis-ci.org/george-silva/django-onivoro.svg?branch=master
    :target: https://travis-ci.org/george-silva/django-onivoro

.. image:: https://codecov.io/gh/george-silva/django-onivoro/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/george-silva/django-onivoro

Allows you to download data from sources and ingest them to your project

Documentation
-------------

The full documentation is at https://django-onivoro.readthedocs.io.

Quickstart
----------

Install Django Onivoro::

    pip install django-onivoro

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'onivoro.apps.OnivoroConfig',
        ...
    )

Add Django Onivoro's URL patterns:

.. code-block:: python

    from onivoro import urls as onivoro_urls


    urlpatterns = [
        ...
        url(r'^', include(onivoro_urls)),
        ...
    ]

Features
--------

* TODO

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

0.1.0 (2017-07-06)
++++++++++++++++++

* First release on PyPI.


