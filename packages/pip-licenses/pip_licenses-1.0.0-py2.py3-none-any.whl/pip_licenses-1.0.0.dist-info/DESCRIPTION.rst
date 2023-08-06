pip-licenses
============

|Build Status| |PyPI version| |GitHub Release| |Codecov| |BSD License|
|Requirements Status|

Dump the license list of packages installed with pip.

Description
-----------

``pip-licenses`` is a CLI tool for checking the software license of
installed packages with pip.

Implemented with the idea inspired by ``composer licenses`` command in
Composer (a.k.a PHP package management tool).

https://getcomposer.org/doc/03-cli.md#licenses

Installation
------------

Install it via PyPI using ``pip`` command.

.. code:: bash

    $ pip install pip-licenses

Usage
-----

Execute the command with your venv (or virtualenv) environment.

.. code:: bash

    # Install packages in your venv environment
    (venv) $ pip install Django pip-licenses

    # Check the licenses with your venv environment
    (venv) $ pip-licenses
     Name    Version  License
     Django  2.0.2    BSD
     pytz    2017.3   MIT

Command-Line Options
--------------------

--with-system
~~~~~~~~~~~~~

By default, system packages such as pip and setuptools are ignored.

If you want to output all including system package, use the
``--with-system`` option.

.. code:: bash

    (venv) $ pip-licenses --with-system
     Name          Version  License
     Django        2.0.2    BSD
     PTable        0.9.2    BSD (3 clause)
     pip           9.0.1    MIT
     pip-licenses  1.0.0    MIT License
     pytz          2017.3   MIT
     setuptools    38.5.0   UNKNOWN

--with-authors
~~~~~~~~~~~~~~

When executed with the ``--with-authors`` option, output with the author
of the package.

.. code:: bash

    (venv) $ pip-licenses --with-authors
     Name    Version  License  Author
     Django  2.0.2    BSD      Django Software Foundation
     pytz    2017.3   MIT      Stuart Bishop

--with-urls
~~~~~~~~~~~

For packages without METADATA, the license is output as ``UNKNOWN``. To
get more package information, use the ``--with-urls`` option.

.. code:: bash

    (venv) $ pip-licenses --with-urls
     Name    Version  License  URL
     Django  2.0.2    BSD      https://www.djangoproject.com/
     pytz    2017.3   MIT      http://pythonhosted.org/pytz

--order
~~~~~~~

By default, it is ordered by package name.

If you give arguments to the ``--order option``, you can output in other
sorted order.

.. code:: bash

    (venv) $ pip-licenses --order=license

More Information
~~~~~~~~~~~~~~~~

Other, please make sure to execute the ``--help`` option.

License
-------

`MIT
License <https://github.com/raimon49/pip-licenses/blob/master/LICENSE>`__

.. |Build Status| image:: https://travis-ci.org/raimon49/pip-licenses.svg?branch=master
   :target: https://travis-ci.org/raimon49/pip-licenses
.. |PyPI version| image:: https://badge.fury.io/py/pip-licenses.svg
   :target: https://badge.fury.io/py/pip-licenses
.. |GitHub Release| image:: https://img.shields.io/github/release/raimon49/pip-licenses.svg
   :target: https://github.com/raimon49/pip-licenses/releases
.. |Codecov| image:: https://codecov.io/gh/raimon49/pip-licenses/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/raimon49/pip-licenses
.. |BSD License| image:: http://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/raimon49/pip-licenses/blob/master/LICENSE
.. |Requirements Status| image:: https://requires.io/github/raimon49/pip-licenses/requirements.svg?branch=master
   :target: https://requires.io/github/raimon49/pip-licenses/requirements/?branch=master


CHANGELOG
---------

1.0.0
~~~~~

-  First stable release version

0.2.0
~~~~~

-  Implement new option ``--order``

   -  Default behavior is ``--order=name``

0.1.0
~~~~~

-  First implementation version

   -  Support options

      -  ``--with-system``
      -  ``--with-authors``
      -  ``--with-urls``


