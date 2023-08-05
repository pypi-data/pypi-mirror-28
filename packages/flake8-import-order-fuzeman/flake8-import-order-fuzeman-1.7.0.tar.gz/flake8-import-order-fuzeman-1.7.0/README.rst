flake8-import-order-fuzeman
===========================

.. image:: https://img.shields.io/pypi/v/flake8-import-order-fuzeman.svg
   :target: https://pypi.python.org/pypi/flake8-import-order-fuzeman

.. image:: https://travis-ci.org/fuzeman/flake8-import-order-fuzeman.svg
   :target: https://travis-ci.org/fuzeman/flake8-import-order-fuzeman

Import ordering style for flake8-import-order_, fork of flake8-import-order-spoqa_ which
has been updated to implement `@fuzeman`__'s preferred import ordering convention.

.. _flake8-import-order: https://github.com/PyCQA/flake8-import-order
.. _flake8-import-order-spoqa: https://github.com/spoqa/flake8-import-order-spoqa

__ https://github.com/fuzeman


Example
-------

.. code-block:: python

    from myapp import something
    from myapp.helpers import get_view
    from myapp.views import *
    from ...deepest import a
    from ..deeper import b
    from .a import this, that
    from .z import This, That

    from pkg_resources import (SOURCE_DIST, EntryPoint, Requirement, get_provider)
    from typing import Optional
    import datetime
    import sys


Usage
-----

Install the ``flake8-import-order-fuzeman`` package with pip_, and then enable the
import order style with either:

- Command-line option:

  .. code-block:: shell

    --import-order-style=fuzeman

- `flake8 configuration file:`__

  .. code-block:: ini

     [flake8]
     import-order-style = fuzeman

.. _pip: https://pip.pypa.io

__ http://flake8.pycqa.org/en/latest/user/configuration.html


Distribution
------------

Written by `Dean Gardiner`__, forked from flake8-import-order-spoqa_ written by `Hong Minhee`__, and
distributed under the GPLv3_ license or later.

.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html

__ https://github.com/fuzeman
__ https://hongminhee.org/


Changelog
---------

1.7.0 (2018-01-08)
~~~~~~~~~~~~~~~~~~

**Added**

- Support for flake8-import-order >= 0.16 *(support has been dropped for earlier versions)*

1.6.0 (2017-05-10)
~~~~~~~~~~~~~~~~~~

**Added**

- ``from ... import ...`` is now permitted for ``contextlib``

1.5.0 (2017-05-10)
~~~~~~~~~~~~~~~~~~

**Added**

- ``from ... import ...`` is now permitted for ``tempfile``

1.4.0 (2017-05-10)
~~~~~~~~~~~~~~~~~~

**Added**

- ``from ... import ...`` is now permitted for ``json`` and ``pkgutil``

1.3.0 (2017-03-07)
~~~~~~~~~~~~~~~~~~

**Added**

- ``from ... import ...`` is now permitted for ``copy``

1.2.0 (2017-02-25)
~~~~~~~~~~~~~~~~~~

**Added**

- ``from ... import ...`` is now permitted for ``argparse``, ``pprint``, ``subprocess`` and ``threading``

1.1.1 (2017-02-22)
~~~~~~~~~~~~~~~~~~

**Fixed**

- Third-party ``import`` statements were incorrectly being marked as import order errors

1.1.0 (2017-02-22)
~~~~~~~~~~~~~~~~~~

**Added**

- ``collections``, ``datetime`` and ``decimal`` are now ``from ...`` importable

**Changed**

- ``import`` is now permitted for third-party libraries

**Fixed**

- ``__future__`` imports were incorrectly being marked as import order errors

1.0.2 (2017-02-22)
~~~~~~~~~~~~~~~~~~

Fix for incorrect metadata on PyPI

1.0.1 (2017-02-22)
~~~~~~~~~~~~~~~~~~

**Fixed**

- Incorrect ``install_requires`` definition in ``setup.py``

1.0.0 (2017-02-22)
~~~~~~~~~~~~~~~~~~

Initial release
