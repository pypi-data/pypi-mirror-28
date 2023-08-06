========
Overview
========



Python client for GitHub API


Installation
============

**requires python 3.6+**

Yes that is opinionated. Python 2 is near the end of the life and this is a new project.

*Note octokit and octokit.py were already taken in the cheese shop*

::

    pip install octokitpy

Documentation
=============

https://octokitpy.readthedocs.io/


Example
-------

::

    from octokit import Octokit

    repos = Octokit.repos.get_for_org(org='octokit', type='public')

Default values::

    TODO Show them

Authentication
--------------

Instatiate a client with the authentication scheme and credentials that you want to use.

Example::

    client = Octokit(type='app', token='xyz')
    client.repos.get_for_org(org='octokit', type='private')

basic::

    TODO

oauth::

    TODO

oauth key/secret::

    TODO

token::

    TODO

app::

    TODO


Pagination
----------

::

    TODO


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

Contributing
============

Pull requests are very welcome!

Please see CONTRIBUTING.md for more information.

Credits
=======

Package based on `cookiecutter-pylibrary <https://github.com/ionelmc/cookiecutter-pylibrary>`_

License
=======

MIT


Changelog
=========

0.1.0 (?)
------------------

* First release on PyPI.


