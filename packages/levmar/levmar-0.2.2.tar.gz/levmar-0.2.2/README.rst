levmar
======
.. image:: http://hera.physchem.kth.se:9090/api/badges/bjodah/levmar/status.svg
   :target: http://hera.physchem.kth.se:9090/bjodah/levmar
   :alt: Build status
.. image:: https://img.shields.io/pypi/v/levmar.svg
   :target: https://pypi.python.org/pypi/levmar
   :alt: PyPI version
.. image:: https://img.shields.io/badge/python-2.7,3.4,3.5-blue.svg
   :target: https://www.python.org/
   :alt: Python version
.. image:: https://img.shields.io/pypi/l/levmar.svg
   :target: https://github.com/bjodah/levmar/blob/master/LICENSE.txt
   :alt: License
.. image:: http://hera.physchem.kth.se/~levmar/branches/master/htmlcov/coverage.svg
   :target: http://hera.physchem.kth.se/~levmar/branches/master/htmlcov
   :alt: coverage

A Python binding to the levmar library. Note that this is a fork of
https://github.com/tkanmae/levmar.


Description
-----------

The levmar is GPL'ed ANSI C implementation of the `Levenberg-Marquardt
(LM) optimization algorithm <https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm>`_.
The LM algorithm provides a numerical solution to the problem of minimizing
a function over a parameter space
of a function.  The levmar library provides implementation of both
unconstrained and constrained LM algorithms (box, linear equation, and
linear inequality constraints).


Installation
------------
Simplest way to install levmar and its dependencies is to use the
`conda pacakge manager <https://conda.pydata.org/docs/>`_::

   $ conda install -c bjodah levmar pytest
   $ python -m pytest --pyargs levmar  # runs the test-suite

alternatively you may also use `pip`::

   $ python -m pip install --user --upgrade pytest levmar
   $ python -m pytest --pyargs levmar

you can skip the ``--user`` flag if you have got root permissions.


Documentation
-------------

See docstrings and demo scripts contained in the directory
``./examples``.  Documentation of the levmar library can be found at
http://www.ics.forth.gr/~lourakis/levmar/. Auto-generated API documentation
for the latest stable release of this wrapper is found here:
`<https://bjodah.github.io/levmar/latest>`_
(and the development version for the current master branch of this wrapper
is found here: `<http://hera.physchem.kth.se/~levmar/branches/master/html>`_).


Authors
-------
Takeshi Kanmae <tkanmae@gmail.com>.
For all authors see `AUTHORS <AUTHORS>`_.


License
-------
The MIT license applies to all the files except those in
``./levmar-2.6``.  All of the software in ``./levmar-2.6`` and only the
software therein is copyrighted by Manolis Lourakis and is licensed
under the terms and conditions of the GNU General Public License (GPL).
See the file `LICENSE.txt <LICENSE.txt>`_.


Resources
---------

* levmar: http://www.ics.forth.gr/~lourakis/levmar/
* Python: http://www.python.org/
* NumPy: http://www.scipy.org/
* nose: http://somethingaboutorange.com/mrl/projects/nose
* Cython: http://www.cython.org/
