Unix: |Build Status| Windows: |Windows Build Status|\ Metrics: |Coverage
Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|

Overview
========

GitMan is a language-agnostic dependency manager using Git. It aims to
serve as a submodules replacement and provides advanced options for
managing versions of nested Git repositories.

|demo|

Setup
=====

Requirements
------------

-  Python 3.5+
-  Git 2.8+ (with `stored
   credentials <http://gitman.readthedocs.io/en/latest/setup/git/>`__)

Installation
------------

Install GitMan with pip:

.. code:: sh

    $ pip install gitman

or directly from the source code:

.. code:: sh

    $ git clone https://github.com/jacebrowning/gitman.git
    $ cd gitman
    $ python setup.py install

Configuration
-------------

Generate a sample config file:

.. code:: sh

    $ gitman init

or manually create one (``gitman.yml`` or ``.gitman.yml``) in the root
of your working tree:

.. code:: yaml

    location: vendor/gitman
    sources:
    - name: framework
      repo: https://github.com/kstenerud/iOS-Universal-Framework
      rev: Mk5-end-of-life
    - name: coverage
      repo: https://github.com/jonreid/XcodeCoverage
      rev: master
      link: Tools/XcodeCoverage
    - name: trufflehog
      repo: https://github.com/dxa4481/truffleHog
      rev: master
      scripts:
      - chmod a+x truffleHog.py
    - name: fontawesome
      repo: https://github.com/FortAwesome/Font-Awesome
      sparse_paths:
      - fonts/*
      rev: master

Ignore the dependency storage location:

.. code:: sh

    $ echo vendor/gitman >> .gitignore

Usage
=====

See the available commands:

.. code:: sh

    $ gitman --help

Updating Dependencies
---------------------

Get the latest versions of all dependencies:

.. code:: sh

    $ gitman update

which will essentially:

#. Create a working tree at ``<root>``/``<location>``/``<name>``
#. Fetch from ``repo`` and checkout the specified ``rev``
#. Symbolically link each ``<location>``/``<name>`` from
   ``<root>``/``<link>`` (if specified)
#. Repeat for all nested working trees containing a config file
#. Record the actual commit SHAs that were checked out (with ``--lock``
   option)
#. Run optional post-install scripts for each dependency

where ``rev`` can be:

-  all or part of a commit SHA: ``123def``
-  a tag: ``v1.0``
-  a branch: ``master``
-  a ``rev-parse`` date: ``'develop@{2015-06-18 10:30:59}'``

Restoring Previous Versions
---------------------------

Display the specific revisions that are currently installed:

.. code:: sh

    $ gitman list

Reinstall these specific versions at a later time:

.. code:: sh

    $ gitman install

Deleting Dependencies
---------------------

Remove all installed dependencies:

.. code:: sh

    $ gitman uninstall

.. |Build Status| image:: https://travis-ci.org/jacebrowning/gitman.svg?branch=develop
   :target: https://travis-ci.org/jacebrowning/gitman
.. |Windows Build Status| image:: https://img.shields.io/appveyor/ci/jacebrowning/gitman/develop.svg
   :target: https://ci.appveyor.com/project/jacebrowning/gitman
.. |Coverage Status| image:: https://img.shields.io/coveralls/jacebrowning/gitman/develop.svg
   :target: https://coveralls.io/r/jacebrowning/gitman
.. |Scrutinizer Code Quality| image:: https://img.shields.io/scrutinizer/g/jacebrowning/gitman.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/gitman/?branch=develop
.. |PyPI Version| image:: https://img.shields.io/pypi/v/GitMan.svg
   :target: https://pypi.python.org/pypi/GitMan
.. |demo| image:: https://raw.githubusercontent.com/jacebrowning/gitman/develop/docs/demo.gif

