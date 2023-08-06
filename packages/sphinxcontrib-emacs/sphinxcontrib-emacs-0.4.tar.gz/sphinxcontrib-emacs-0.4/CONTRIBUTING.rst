=========================
 Contribution guidelines
=========================

.. default-role:: code

If you discovered bugs and issues, have ideas for improvements or new features,
or want to contribute a new syntax checker, please report to the `issue
tracker`_ the repository and send a pull request, but respect the following
guidelines.

.. _reporting-issues:

Reporting issues
================

- Check that the issue has not already been reported.
- Check that the issue has not already been fixed in the latest code.
- Be clear and precise (do not prose, but name functions and commands exactly).
- Include the version of sphinxcontrib-emacs.
- Open an issue with a clear title and description in grammatically correct,
  complete sentences.

.. _contributing-code:

Contributing code
=================

Contributions of code, either as pull requests or as patches, are *very*
welcome, but please respect the following guidelines.

General
-------

- Write good and *complete* code.
- Provide use cases and rationale for new features.

Code style
----------

- Respect :pep:`8`.
- Make sure that your code does not introduce Pylint_ warnings, using
  ``.pylintrc`` in the top-level source directory.  Flycheck_ will help here.
- Add docstrings for every declaration, following :pep:`257`.  Use Sphinx_
  markup in docstrings.

.. _Pylint: http://www.pylint.org/
.. _flycheck: http://flycheck.readthedocs.org/en/latest/
.. _Sphinx: http://sphinx-doc.org/

Commit messages
---------------

Write commit messages according to `Tim Pope's guidelines`_. In short:

- Start with a capitalized, short (50 characters or less) summary, followed by a
  blank line.
- If necessary, add one or more paragraphs with details, wrapped at 72
  characters.
- Use present tense and write in the imperative: “Fix bug”, not “fixed bug” or
  “fixes bug”.
- Separate paragraphs by blank lines.
- Do *not* use special markup (e.g. reST or Markdown).  Commit messages are
  plain text.  You may use ``*emphasis*`` or ``_underline_`` though, following
  conventions established on mailing lists.

This is a model commit message::

    Capitalized, short (50 chars or less) summary

    More detailed explanatory text, if necessary.  Wrap it to about 72
    characters or so.  In some contexts, the first line is treated as the
    subject of an email and the rest of the text as the body.  The blank
    line separating the summary from the body is critical (unless you omit
    the body entirely); tools like rebase can get confused if you run the
    two together.

    Write your commit message in the imperative: "Fix bug" and not "Fixed bug"
    or "Fixes bug."  This convention matches up with commit messages generated
    by commands like git merge and git revert.

    Further paragraphs come after blank lines.

    - Bullet points are okay, too

    - Typically a hyphen or asterisk is used for the bullet, followed by a
      single space, with blank lines in between, but conventions vary here

    - Use a hanging indent

`Git Commit Mode`_ and Magit_ provide a major mode for Git commit messages,
which helps you to comply to these guidelines.

.. _pull requests:

Pull requests
-------------

- Use a **topic branch** to easily amend a pull request later, if necessary.
- Do **not** open new pull requests, when asked to improve your patch.  Instead,
  amend your commits with `git rebase -i`, and then update the pull request with
  `git push --force`
- Open a `pull request`_ that relates to but one subject with a clear title and
  description in grammatically correct, complete sentences.

.. _issue tracker: https://github.com/sambrightman/sphinxcontrib-emacs/issues
.. _Tim Pope's guidelines: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
.. _Git Commit Mode: https://github.com/magit/git-modes/
.. _Magit: https://github.com/magit/magit/
.. _pull request: https://help.github.com/articles/using-pull-requests
