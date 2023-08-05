==========
git-upload
==========

.. image:: https://circleci.com/gh/masayukig/git-upload.svg?style=shield
    :target: https://circleci.com/gh/masayukig/git-upload

.. image:: https://img.shields.io/pypi/v/git-upload.svg
    :target: https://pypi.python.org/pypi/git-upload


I don't want to care about the type of repositories when pushing a
patch.


Description
===========

When you use this ``git upload`` command in a repo managed by Gerrit
(supported only OpenStack repos, currently), this command runs ``git
review`` . And when you use this command in a repo managed by the
others, this command runs ``git push origin $CURRENT_BRANCH`` (you can
specify the remote repo and branch, of course :).


Installation
============

From source
-----------

::

   $ git clone https://github.com/masayukig/git-upload
   $ cd git-upload
   $ sudo pip install -e .
   or
   $ virtualenv ~/venv; source ~/venv/bin/activate; pip install .

From PYPI
---------

::

   $ pip install git-upload
   or
   $ virtualenv ~/venv; source ~/venv/bin/activate; pip install git-upload

Usage
=====

::

   $ git upload [<remote-repo>] [<branch>]
   or you can use varioush options for `git push` or `git review`.



