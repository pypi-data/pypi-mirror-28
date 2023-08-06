FactorDB CLI (and Python library)
=================================

|CircleCI| |PyPI| |PyPI| |PyPI| |PyPI| |Codecov|

The `FactorDB`_ is the database to store known factorizations for any
number. This tool can use on your command line. And also you can use
this tool with python 2 & 3 scripts.

Installation
------------

The easiest way to install factordb-pycli is to use `pip`_:

.. code:: bash

    $ pip install factordb-pycli

or, if you are not installing in a ``virtualenv``:

.. code:: bash

    $ sudo pip install factordb-pycli

If you have the factordb-pycli installed and want to upgrade to the
latest version you can run:

.. code:: bash

    $ pip install --upgrade factordb-pycli

Getting Started
---------------

CLI
~~~

If you want to know the result of factorization of 16, you should type
like this:

.. code:: bash

    $ factordb 16

Then, you can get the answer from factordb.com.

.. code:: bash

    $ factordb 16
    2 2 2 2

If you want to know more detail of result, you can get an answer of JSON
format.

.. code:: bash

    $ factordb --json 16
    {"id": "http://factordb.com/?id=2", "status": "FF", "factors": [2, 2, 2, 2]}

Library usage
~~~~~~~~~~~~~

If you want to use this script with Python, you should type ``import``
statement on your code like this:

::

    from factordb.factordb import FactorDB

Then, you can get the answer with Python lists.

::

    In [1]: from factordb.factordb import FactorDB

    In [2]: f = FactorDB(16)

    In [3]: f.get_factor_list()
    Out[3]: []

    In [4]: f.connect()
    Out[4]: <Response [200]>

    In [5]: f.get_factor_list()
    Out[5]: [2, 2, 2, 2]

    In [6]: f.get_factor_from_api()
    Out[6]: [['2', 4]]

    In [7]: f.get_status()
    Out[7]: 'FF'

License
=======

MIT

.. _FactorDB: https://factordb.com
.. _pip: http://www.pip-installer.org/en/latest/

.. |CircleCI| image:: https://img.shields.io/circleci/project/github/ryosan-470/factordb-pycli.svg?style=flat-square
   :target: https://circleci.com/gh/ryosan-470/factordb-pycli
.. |PyPI| image:: https://img.shields.io/pypi/l/factordb-pycli.svg?style=flat-square
   :target: ./LICENSE.md
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/factordb-pycli.svg?style=flat-square
   :target: https://pypi.python.org/pypi/factordb-pycli
.. |PyPI| image:: https://img.shields.io/pypi/status/factordb-pycli.svg?style=flat-square
   :target: https://pypi.python.org/pypi/factordb-pycli
.. |PyPI| image:: https://img.shields.io/pypi/v/factordb-pycli.svg?style=flat-square
   :target: https://pypi.python.org/pypi/factordb-pycli
.. |Codecov| image:: https://img.shields.io/codecov/c/github/ryosan-470/factordb-pycli.svg?style=flat-square
   :target: https://codecov.io/gh/ryosan-470/factordb-pycli
