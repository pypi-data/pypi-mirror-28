.. _index:

===================
Django Crashlog
===================

Django application to log into the database any Exception that occurs into the application.
Each exception is available in the Admin, with the same layout of the Django debug page


Install
======================

configure your settings.py

.. code-block::python

    INSTALLED_APPS = (
        ....,
        'crashlog'
    )

    MIDDLEWARE_CLASSES = (
        ....,
        'crashlog.middleware.CrashLogMiddleware',
    )

Avoid logging of exceptions
============================================

To skip logging of specific exception, configure your ``settings`` as below

.. code-block::python

    CRASHLOG_IGNORE_EXCEPTIONS = ('module.name.Exception',)


Changelog
=========

.. toctree::
    :maxdepth: 2


    changes

