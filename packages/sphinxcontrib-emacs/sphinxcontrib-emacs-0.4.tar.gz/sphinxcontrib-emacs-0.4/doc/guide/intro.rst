==============
 Introduction
==============

sphinxcontrib-emacs is an extension to the Sphinx_ documentation tool, which
lets you document Emacs Lisp symbols, including automatic docstring extraction
from Emacs Lisp source.

This page gives you brief overview of Sphinx and its underlying markup
reStructuredText.

Sphinx
======

Sphinx forms the base this extension builds on.  It is a powerful documentation
processor, initially created by the Python Foundation for the `Python
documentation`_.

It supports many different output formats (including HTML, PDF and Texinfo), has
extensive cross-referencing support, automated index generation, and a powerful
interface for custom extensions.

More information about Sphinx can be found in the `Sphinx documentation`_.  If
you are not familiar with Sphinx, please take a look at the `Introduction`_, and
read the tutorial_.

.. _Python documentation: https://docs.python.org/3/
.. _Sphinx documentation: http://sphinx-doc.org/
.. _Introduction: http://sphinx-doc.org/intro.html
.. _Tutorial: http://sphinx-doc.org/tutorial.html

reStructuredText
================

Sphinx uses reStructuredText_ (:abbr:`ReST (reStructuredText)`) as markup for
documentation sources.  It is an easy-to-use plaintext markup, similar to the
popular Markdown format, but with a more regular grammar, and extensible syntax.

The Sphinx documentation has a brief, but comprehensive :ref:`rst-primer`, which
should get you started on reST if you are familiar with similar formats like
Markdown.  More information can be found on the reStructuredText_ page,
including a `specification`_ and a reference of the provided directives_ and
roles_.

Sphinx adds its own special markup to reStructuredText, for the specific needs
of large documentation.  This markup is documented in :ref:`sphinxmarkup`.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _specification: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _directives: http://docutils.sourceforge.net/docs/ref/rst/directives.html
.. _roles: http://docutils.sourceforge.net/docs/ref/rst/roles.html
