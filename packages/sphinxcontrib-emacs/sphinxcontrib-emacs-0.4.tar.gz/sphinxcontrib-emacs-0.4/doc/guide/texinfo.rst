=================
 Texinfo support
=================

.. default-domain:: rst

This page documents the special Texinfo support offered by this extension.

Introduction
============

Emacs users expect to have documentation available as Info manuals, to read and
browse documentation with Emacs' Info viewer without having to leave
Emacs.  Sphinx provides a :py:class:`Texinfo builder
<sphinx.builders.texinfo.TexinfoBuilder>` to generate a Texinfo_ file, which can
be feed to `makeinfo` 4.x and upwards.  While the results are not as perfect as
a manually written Texinfo manual, they are good enough for daily use.

.. _Texinfo: http://www.gnu.org/software/texinfo/

Setup
=====

To generate Texinfo documentation, you need tell the Texinfo builder which
documents to include into the manual, by setting :confval:`texinfo_documents` in
:file:`conf.py`:

.. code-block:: python

   texinfo_documents = [('index', 'hello', '', 'John Doe',
                         'hello', 'Hello world for GNU Emacs', 'Emacs',
                         False)]

Assuming that ``index.rst`` is the root document, this will include the entire
documentation in the Info manual.  Typically, though, this is not what you want,
since some parts of your documentation will be specific to HTML, such as a nice
front page with a screenshot to “advertise” your project.

Hence, you may want to include only the actual manual in the Info manual:

.. code-block:: python

   texinfo_documents = [('manual', 'hello', '', 'John Doe',
                         'hello', 'Hello world for GNU Emacs', 'Emacs',
                         False)]

To fine-tune the Texinfo output, take a look at the other
:ref:`texinfo-options`.

Referencing Info manuals
========================

To reference pages (“nodes”) in other Info manuals, use the special
:role:`infonode` role:

.. role:: infonode

   Reference a node in an Info manual.

   The text of this role has the form :samp:`({manual}){node}`, where ``manual``
   is the name of the Info manual, and ``node`` the name of the target node in
   ``manual``.  For instance, ``:infonode:`(emacs)Intro``` references the
   `Introduction`_ of the `GNU Emacs manual`_: :infonode:`(emacs)Intro`.

   When generating Texinfo output, this role creates a special Info reference.
   For other output formats, this role creates a standard reference to the
   online version of the Info manual.

   The online version of the Info manual is looked up in the latest `Info manual
   database`_ of Texinfo.  Use :confval:`info_xref` to add explicit entries to
   the database.

   .. _Introduction: http://www.gnu.org/software/emacs/manual/html_node/emacs/Intro.html#Intro
   .. _GNU Emacs manual: http://www.gnu.org/software/emacs/manual/html_node/emacs/index.html
   .. _Info manual database: http://ftpmirror.gnu.org/texinfo/htmlxref.cnf

.. confval:: info_xref

   Additional Info manuals for cross-referencing.

   The value is a dictionary, mapping the name of a manual to the **root URL**
   of the split HTML version, i.e. the HTML version that has a single page per
   node.

   For instance, the following setting adds the manual of ERT, the Emacs unit
   testing library:

   .. code-block:: python

      info_xref = {'ert': 'http://www.gnu.org/software/emacs/manual/html_node/ert/'}

   Entries in this configuration value override entries retrieved from the
   online database.  The online database is still consulted for other manuals,
   though.

In Info manuals these special references have a couple of advantages over a
standard reference to the online version of the referenced manual:

- The Info reader of GNU Emacs can follow these references directly inside
  Emacs, without the need for a proper Web browser, and keeps a consistent
  navigation history across references.  For instance, when following a
  reference to the Emacs manual, the user can press :kbd:`L` in the Emacs manual
  to get back to the reference.
- The references work without a network connection, because Info manuals are
  stored on disk and can be read and browsed offline.

Hence, the experience of using your manual in Emacs is more consistent with
these special references.

The downside is that you can only reference nodes in other manuals, but no
entities within nodes, i.e. you can reference the
:infonode:`(elisp)Sequence Functions` node in the Emacs Lisp reference, but not the
documentation of the nreverse_ function in this node.

.. _nreverse: http://www.gnu.org/software/emacs/manual/html_node/elisp/Sequence-Functions.html#index-nreverse-433

Special inline markup
=====================

The following roles let you denote metavariables, which get special rendering in
Info manuals.  They are typically used to refer to parameters of functions.

.. role:: var

   Denote a metavariable.

   In HTML, the text of this role is enclosed in a ``var`` tag.  In Texinfo, it
   is rendered using the ``@var`` macro.

.. role:: varcode

   Like :role:`samp`, but denote text in curly braces as metavariable (as in
   :role:`var`) instead of emphasizing it.
