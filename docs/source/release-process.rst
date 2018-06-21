Release Process
===============

Outcomes
--------

* A new ``git`` tag available to install.
* An updated `Homebrew`_ recipe.
* The new version title in the changelog.

Prerequisites
-------------

* ``python3`` on your ``PATH`` set to Python 3.5+.
* ``virtualenv``.
* Push access to this repository.
* Trust that ``master`` is ready and high enough quality for release.
  This includes the ``Next`` section in ``CHANGELOG.rst`` being up to date.

Perform a Release
-----------------

#. Get a GitHub access token:

   Follow the `GitHub instructions <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`__ for getting an access token.

#. Set environment variables to GitHub credentials, e.g.:

    .. code:: sh

       export GITHUB_TOKEN=75c72ad718d9c346c13d30ce762f121647b502414

#. Perform a release:

    .. code:: sh

       curl https://raw.githubusercontent.com/dcos/dcos-e2e/master/admin/release.sh | bash

.. _Homebrew: https://brew.sh/
