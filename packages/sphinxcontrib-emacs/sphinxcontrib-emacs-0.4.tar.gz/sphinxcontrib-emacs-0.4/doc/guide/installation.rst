==============
 Installation
==============

This document covers the installation and setup of this extension.

Installing the package
======================

As sphinxcontrib-emacs is available in Python's package repository, you can
easily install it with pip_, Python's package manager:

.. code-block:: console

   $ pip install sphinxcontrib-emacs

.. _pip: http://www.pip-installer.org/en/latest/
.. _virtualenv: http://www.virtualenv.org/en/latest/

Enabling the extension
======================

To enable this extension, simply add it to :confval:`extensions` in your
:file:`conf.py`:

.. code-block:: python

   extensions = ['sphinx.ext.intersphinx',
                 'sphinxcontrib.emacs']
