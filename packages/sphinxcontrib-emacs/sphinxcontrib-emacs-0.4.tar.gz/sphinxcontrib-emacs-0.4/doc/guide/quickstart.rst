=======================
 Quickstart by example
=======================

This page gets you started quickly with sphinxcontrib-emacs, by an simple
example.  It assumes

- that you are already familiar with Sphinx,
- and have Sphinx and sphinxcontrib-emacs installed.

Thus, this page will only go through the specific setup and features of
sphinxcontrib-emacs.  Consult the `Sphinx documentation`_ for information about
Sphinx.

.. _Sphinx documentation: http://sphinx-doc.org

.. warning::

   If you are not familiar with Sphinx, please go through the `Sphinx tutorial`_
   first.

   .. _Sphinx tutorial: http://sphinx-doc.org/tutorial.html

.. _sample-project-layout:

The project layout
==================

We want to document a simple :file:`hello.el` library, which implements the good
old Hello world program.

Our project has the following layout::

   README.md
   hello.el

:file:`hello.el` is very simple, with just one command, and a user option:

.. literalinclude:: ../sample/hello.el
   :language: cl
   :linenos:

Setup
=====

We create a subdirectory :file:`doc/` for our documentation, and go through the
:program:`sphinx-quickstart` tool, which gives us a skeleton for our
documentation::

   doc/conf.py
   doc/index.rst
   doc/Makefile
   doc/make.bat

:file:`doc/conf.py` is the :ref:`build configuration <build-config>`.  Here we
enable sphinxcontrib-emacs by adding it to the :confval:`extensions` setting:

.. code-block:: python

   # Add any Sphinx extension module names here, as strings. They can be
   # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
   # ones.
   extensions = ['sphinxcontrib.emacs']

Documenting commands
====================

We start with documenting the interactive command, the most important feature of
our `hello` library.

We create a separate document :file:`doc/hello.rst` for the documentation of the
`hello` library, and add it to the :ref:`TOC tree <toctree-directive>` in
:file:`doc/index.rst`:

.. code-block:: rst

   .. toctree::
      :maxdepth: 2

      hello

In :file:`doc/hello.rst` we can now document the `hello` command:

.. code-block:: rst

   ===================
    The hello library
   ===================

   Greet users.

   .. el:command:: greet
      :binding: C-c g

      Prompt for the name of a user and greet them.

      Use :el:option:`greeting` to change the greeting text.

``:el:option:`greeting``` inserts a cross-reference to the documentation of
the ``greeting`` option, which we add :ref:`further down <quickstart-options>`.

In `hello.el`, we install global key binding :kbd:`C-c g` for our command, so we
document this additional binding in the ``:binding:`` option.  This binding now
appears in the documentation of the ``greet`` command:

.. el:command:: greet
   :binding: C-c g

   Prompt for the name of a user and greet them.

   Use :el:option:`greeting` to change the greeting text.

Documenting different invocations of commands
=============================================

In Emacs Lisp, any command is a function as well, which can be called from Emacs
Lisp.  To account for this, we also want to document the function “aspect” of
:el:command:`greet`:

.. code-block:: rst

   .. el:function:: greet name
      :noindex:

      Greet the user with the given ``name``.

      ``name`` is a string identifying the user to greet.

.. el:function:: greet name
   :noindex:

   Greet the user with the given ``name``.

   ``name`` is a string identifying the user to greet.

We use the ``:noindex:`` option to suppress the index entry and cross-reference
target, since we have already documented the ``greet`` symbol as command.

In the documentation index, and in cross-references, ``greet`` will always refer
to the interactive command, documented above.

Auto-documenting functions
==========================

When documenting ``greet`` as a function, we wrote an explicit documentation.
However, we already have documentation, in the docstring of ``greet``:

.. literalinclude:: ../sample/hello.el
   :language: cl
   :linenos:
   :lines: 12-22

To avoid this duplication, we change our documentation to extract the docstring
of the `greet` function.

First, we need to point sphinxcontrib-emacs to the Emacs Lisp source file, by
changing appending the following to :file:`doc/conf.py`:

.. code-block:: python

   emacs_lisp_load_path = [
       os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
   ]

This tells sphinxcontrib-emacs, that Emacs Lisp source files are to be found in
the parent directory of the documentation (remember our :ref:`project layout
<sample-project-layout>`).  By using :py:func:`os.path.join` and
:py:data:`os.pardir`, we ensure that our documentation builds regardless of
where we checked out our project.

Then we load the `hello` library to make its docstrings available, by adding the
following to the top of :file:`doc/hello.rst`:

Now we use the docstring of `greet` as documentation of the ``greet`` function:

.. code-block:: rst

   .. el:require:: hello

   .. el:function:: greet
      :noindex:
      :auto:

.. el:require:: hello

.. el:function:: greet
   :noindex:
   :auto:

We remove our manually written documentation, and instead add the ``:auto:``
option to have docstring of `greet` inserted as documentation.  Note that we
also removed the argument name, since ``:auto:`` will also extract the function
signature.

In docstrings, only the markup of Help Mode is parsed (see
:infonode:`(elisp)Documentation Tips`).  reST is not supported.

.. note::

   The peculiar layout and presentation of extracted docstrings is to maintain
   compatibility with the limited markup and presentation of docstrings in
   Emacs' Help Mode.

.. _quickstart-options:

Auto-documenting options
========================

Now we can also automatically document the ``greeting`` option:

.. code-block:: rst

   .. el:option:: greeting
      :auto:

Using ``:auto:`` for variables will automatically add the variables properties
as well.  Remember the definition of ``greeting``:

.. literalinclude:: ../sample/hello.el
   :language: cl
   :linenos:
   :lines: 1-10

The variable is marked as safe for string values, and as buffer-local.  These
properties are reflected in the documentation.  The package version is recorded
as well:

.. el:option:: greeting
   :auto:

Further reading
===============

- :doc:`domain` describes directives and roles to document Emacs Lisp symbols.
- :doc:`autodoc` has details on auto-documenting Emacs Lisp symbols.
