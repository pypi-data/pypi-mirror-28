cplot
=====

Plotting complex-valued functions.

|CircleCI| |codecov| |PyPi Version| |GitHub stars|

cplot is an attempt at encoding complex-valued data in colors. The
general idea is to map the absolute value to lightness and the complex
argument (the "angle") to the chroma.

.. code:: python

    import cplot
    import numpy

    cplot.show(numpy.tan, -5, +5, -5, +5, 100, 100)

produces

.. figure:: https://nschloe.github.io/cplot/tan.png
   :alt: 
   :width: 30.0%

Testing
~~~~~~~

To run the cplot unit tests, check out this repository and type

::

    pytest

Distribution
~~~~~~~~~~~~

To create a new release

1. bump the ``__version__`` number,

2. tag and upload to PyPi:

   ::

       make publish

License
~~~~~~~

cplot is published under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

.. |CircleCI| image:: https://img.shields.io/circleci/project/github/nschloe/cplot/master.svg
   :target: https://circleci.com/gh/nschloe/cplot/tree/master
.. |codecov| image:: https://img.shields.io/codecov/c/github/nschloe/cplot.svg
   :target: https://codecov.io/gh/nschloe/cplot
.. |PyPi Version| image:: https://img.shields.io/pypi/v/cplot.svg
   :target: https://pypi.python.org/pypi/cplot
.. |GitHub stars| image:: https://img.shields.io/github/stars/nschloe/cplot.svg?style=social&label=Stars
   :target: https://github.com/nschloe/cplot


