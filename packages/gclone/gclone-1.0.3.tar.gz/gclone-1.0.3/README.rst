gclone
======
Python 3 program for cloning github repositories by name or keyword.

Install
-------
``pip install --user gclone``

Ensure script location is in your ``PATH``. Usually ``~/.local/bin``.

Usage
-----

Clone by repo name::

  $ gclone mtbrock/gclone

Clone by partial name or keyword. gclone provides a list of github
repositories to choose from, sorted by 'stars'::

  $ gclone tmux

Pass options like you would to ``git clone``::

  $ gclone --branch my-branch my-repo /path/to/my-dir

Specify sort, order, or limit::

  $ gclone --sort='forks' --order='desc' --limit=20 keyword
