Installation
============

CPG can be installed from its source code available at its `GitLab`_
repository.  Install CPG by running the following command from the source code
directory::

  $ pip install .

.. _GitLab: https://gitlab.com/9f/cpg


Generating Documentation
========================

Generate the documentation by running the following commands from CPG's source
code directory::

  $ pip install sphinx
  $ python setup.py build_sphinx

The built documentation can be accessed from the source code directory at
``docs/_build/html/index.html``.


Running Tests
=============

Tests can be run by executing the following command from CPG's source code
directory::

  $ python setup.py test
