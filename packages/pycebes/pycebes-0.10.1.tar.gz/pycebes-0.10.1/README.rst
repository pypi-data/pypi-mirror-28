============
cebes-python
============

Python client for Cebes - an integrated framework for Data Science.

See `Cebes website <https://cebes.github.io>`_ and
`cebes-server <https://github.com/cebes/cebes-server>`_ for more information.

Installation
============

`pycebes` is a pure Python package and can be installed from PyPI:

::

    $ pip install pycebes

Unit tests
==========

::

    $ pip install nose coverage
    $ nosetests --with-coverage --cover-package=pycebes --cover-html --cover-html-dir=tests/report tests/test_*

Python versions
===============

Python >= 2.7 and >= 3.3 are supported. Other older versions might work too, but they are not actively tested.

Contributing
============

If you'd like to contribute, fork the project, make a patch and send a pull request.

In general, we keep track features in the main `cebes-server <https://github.com/cebes/cebes-server>`_ repository.
Create an issue on this repository only if it is ``pycebes``-specific.
