=============================================
 Extracting docstrings of Emacs Lisp symbols
=============================================

.. default-domain:: rst

sphinxcontrib-emacs can extract docstrings from Emacs Lisp libraries, and use
them in your documentation.

This page explains the advantages and drawbacks of this approach, and guides you
through setup and usage.

.. warning::

   When extracting docstrings from Emacs Lisp source code, be sure to respect
   the license of the corresponding source code, which covers the docstrings as
   well.

Pros and cons
=============

Re-using docstrings for documentation avoids duplication and provides consistent
information regardless of whether a user reads your documentation or the
docstring right in Emacs.  This comes at a price however, and there are two
major drawbacks.

.. _interpreter-limits:

Limits of the interpreter
-------------------------

To avoid an external dependency onto `emacs`, sphinxcontrib-emacs uses a custom
Emacs Lisp reader and interpreter to extract docstrings.  This reader and
interpreter is limited in what it supports:

- Static top-level definitions like `defun`, `defvar`, `defcustom` and friends.
- Top-level `put` and related forms (e.g. `make-variable-buffer-local`) with
  static arguments, that is, quoted symbols and literal primitives
- Body forms of `eval-and-compile`, `progn`, and related forms

Notably, it does **not** expand macros, inspect the body forms of definitions or
track the values of variables.

While this limited reader and interpreter is usually sufficient to extract
docstrings, since definitions tend to be static in Emacs Lisp, but it will
obviously fail in specific cases:

- Nested definitions, e.g. a `defun` within a `defun`.
- Definitions in macro expansions, e.g. a `defvar` expanded by a custom macro.
- Manually assembled definitions, e.g. explicitly setting the function cell of a
  symbol and its `function-documentation` property.

In these cases, sphincontrib-emacs will fail to properly extract docstrings.  As
of now, there is no way to work around these limitations, other than writing
documentation manually.

Primitive markup of docstrings
------------------------------

To ensure compatibility with the limited markup and presentation capabilities of
Emacs' Help Mode, sphinxcontrib-emacs shows docstrings as literal block of text,
and does not parse reST markup inside docstrings.  Only references as documented
in :infonode:`(elisp)Documentation Tips` are handled.

.. note::

   Key binding substitutions (see :infonode:`(elisp)Keys in Documentation`) are
   **not** substituted, since the limited Emacs Lisp interpreter used by this
   extension does not track the values of keymaps (see
   :ref:`interpreter-limits`).

Thus, extracted docstrings look somewhat “ugly” compared to manually written
documentation.

Loading the Emacs Lisp source
=============================

To use docstrings from Emacs Lisp source, you first need to load the
corresponding Emacs Lisp source file with :dir:`el:require` from the :ref:`Emacs
Lisp domain <el-domain>`:

.. directive:: .. el:require:: feature

   Load the given ``feature`` to make its docstrings available for
   auto-documenting Emacs Lisp symbols.  ``feature`` is a feature symbol, like
   in the Emacs function `require`.

   sphinxcontrib-emacs searches for the corresponding source file in
   :confval:`emacs_lisp_load_path`, which is similar to Emacs' `load-path`.

   .. note::

      You must put :dir:`el:require` **before** the first auto-documented Emacs
      Lisp symbol in a file.  Also, you must add the necessary :dir:`el:require`
      directives to **every** file which uses docstrings from an Emacs Lisp
      source.

:dir:`el:require` searches for source files in :confval:`emacs_lisp_load_path`:

.. confval:: emacs_lisp_load_path

   A list of directories where to look for Emacs Lisp sources.

Set this in your :file:`conf.py`, to point sphinxcontrib-emacs to the location
of the Emacs Lisp source whose docstrings you want to use.  For instance, if
your Emacs Lisp library sits in the top-level source directory, and your
:file:`conf.py` in the subdirectory :file:`doc/`, you would add the following to
:file:`conf.py`:

.. code-block:: python

   import os

   emacs_lisp_load_path = [
       os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
   ]

Using docstrings
================

To insert the docstring of a symbol, add the ``:auto:`` flag to the
corresponding directive:

.. code-block: rst

   .. el:variable:: foo
      :auto:

.. warning::

   Currently, :dir:`el:cl-struct` and :dir:`el:cl-slot` do not support
   ``:auto:`` properly.

With ``auto``, all directives from the :ref:`Emacs Lisp domain <el-domain>` will

- insert the docstring of the symbol before any additional content of the
  directive,
- and add a :dir:`versionchanged` annotation if appropriate.

:dir:`el:function` will also extract the function signature from the Emacs Lisp
source.  Any custom signature is *ignored*.

Furthermore, :dir:`el:variable`, :dir:`el:option` and :dir:`el:hook` insert
annotations concerning the properties of a variable:

- Whether the variable is buffer local or not.
- Whether the variable is safe or risky as a file-local variable.
