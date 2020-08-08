.. _development:

Development
===========

Links
-----

The source code for ``ssds`` is released under the `Apache License 2.0`_.
It can be viewed on Github under the project `ssds-python`_. In PyPI,
it can be viewed at `ssds`_.

``ssds-python`` also has a sister project: ``ssds-deno``, a version of the
library ported to Deno. The same algorithmic efficiency for all your Deno
back-end needs! It is also released under the Apache License 2.0 and
can be viewed on Github (`ssds-deno`_).

Currently, all the data structures in ``ssds-python`` are implemented in
Python for ease of programming. Later, they may be re-implemented in C
for efficiency.

Testing
-------

``ssds`` comes with an array of unit tests. They can be run on a
file-by-file basis by using the following command format:

.. code-block::

   python3 -m unittest tests/<filename>.py

There are two categories of
tests: accuracy and efficiency. Accuracy tests compare the ``ssds`` data
structure against a naive implementation for correctness; efficiency tests
simply time how long it takes to execute a series of operations.


.. _Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
.. _ssds-python: https://github.com/claytsay/ssds-python
.. _ssds-deno: https://github.com/claytsay/ssds-deno
.. _ssds: https://pypi.org/project/ssds/
