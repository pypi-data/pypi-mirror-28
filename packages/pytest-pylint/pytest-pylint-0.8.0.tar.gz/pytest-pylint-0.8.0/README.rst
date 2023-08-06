pytest pylint
-------------
.. image:: https://img.shields.io/travis/carsongee/pytest-pylint.svg
    :target: https://travis-ci.org/carsongee/orcoursetrion
.. image:: https://img.shields.io/coveralls/carsongee/pytest-pylint.svg
    :target: https://coveralls.io/r/carsongee/pytest-pylint
.. image:: https://img.shields.io/pypi/v/pytest-pylint.svg
    :target: https://pypi.python.org/pypi/pytest-pylint
.. image:: https://img.shields.io/pypi/dm/pytest-pylint.svg
    :target: https://pypi.python.org/pypi/pytest-pylint
.. image:: https://img.shields.io/pypi/l/pytest-pylint.svg
    :target: https://pypi.python.org/pypi/pytest-pylint

Run pylint with pytest and have configurable rule types
(i.e. Convention, Warn, and Error) fail the build.  You can also
specify a pylintrc file.

Sample Usage
============
.. code-block:: shell

   py.test --pylint

would be the most simple usage and would run pylint for all error messages.

.. code-block:: shell

   py.test --pylint --pylint-rcfile=/my/pyrc --pylint-error-types=EF

This would use the pylintrc file at /my/pyrc and only error on pylint
Errors and Failures.

You can restrict your test run to only perform pylint checks and not any other
tests by typing:

.. code-block:: shell

    py.test --pylint -m pylint

Acknowledgements
================

This code is heavily based on 
`pytest-flakes <https://github.com/fschulze/pytest-flakes>`_


Releases
========

0.8.0
~~~~~

- `bdrung <https://github.com/bdrung>`_ corrected inconsitent returns in a function
- Dropped Python 3.3 support

0.7.1
~~~~~

- Corrected path issue reported by `Kargathia <https://github.com/Kargathia>`_

0.7.0
~~~~~

- Linting is performed before tests which enables code duplication
  checks to work along with a performance boost, thanks to @heoga
