shleem
########
|PyPI-Status| |PyPI-Versions| |Build-Status| |Codecov| |LICENCE|

Automate and version datasets generation from data sources.

.. code-block:: python

  import shleem
  # mystery code

.. contents::

.. section-numbering::


Installation
============

.. code-block:: bash

  pip install shleem


Setting up shleem
===================

shleem uses a couple of simple conventions to handle credentials and refer to MongoDB servers:

Credentials file
----------------

You must set up a credentials file for shleem to use. Create a ``.shleem/shleem_credentials.yml`` file in your home folder, populating it with your MongoDB credentials, using an identical structure to the inner structure of the ``envs`` configuration parameters:

.. code-block:: python

  environment_name:
    server_name:
      reading:
        username: reading_username
        password: password1
      writing:
        username: writing_username
        password: password2

You can extend this to include any number of environments and servers.


Basic Use
=========

Pass.


Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.

Installing for development
----------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:shaypal5/shleem.git


Install in development mode:

.. code-block:: bash

  cd shleem
  pip install -e .


Running the tests
-----------------

To run the tests use:

.. code-block:: bash

  pip install pytest pytest-cov coverage
  cd shleem
  pytest


Adding documentation
--------------------

The project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings. When documenting code you add to this project, follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Credits
=======

Created by Shay Palachy (shay.palachy@gmail.com).


.. |PyPI-Status| image:: https://img.shields.io/pypi/v/shleem.svg
  :target: https://pypi.python.org/pypi/shleem

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/shleem.svg
   :target: https://pypi.python.org/pypi/shleem

.. |Build-Status| image:: https://travis-ci.org/shaypal5/shleem.svg?branch=master
  :target: https://travis-ci.org/shaypal5/shleem

.. |LICENCE| image:: https://img.shields.io/pypi/l/shleem.svg
  :target: https://pypi.python.org/pypi/shleem

.. |Codecov| image:: https://codecov.io/github/shaypal5/shleem/coverage.svg?branch=master
   :target: https://codecov.io/github/shaypal5/shleem?branch=master

