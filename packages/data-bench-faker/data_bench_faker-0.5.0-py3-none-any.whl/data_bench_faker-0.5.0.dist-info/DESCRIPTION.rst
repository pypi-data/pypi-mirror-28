Data Bench Faker
================

|pypi| |license| |python|

**data_bench_faker** is a provider for the `Faker`_ Python package
which creates stable, scalable data for the `Data Bench`_ benchmark.

Install
-------

Install with pip:

.. code:: bash

 $ pip install data-bench-faker


Or install with setup.py:

.. code:: bash

 $ git clone https://github.com/erikoshaughnessy/data-bench-faker.git
 $ cd data-bench-faker && python3 setup.py install

Uninstall with pip:

.. code:: bash

	  $ pip uninstall data-bench-faker

Usage
-----

Add the ``DataProvider`` to your ``Faker`` instance:

.. code:: python

	  from faker import Faker
	  from data_bench_faker import DataProvider

	  fake = Faker()
	  fake.add_provider(DataProvider)

	  customer = fake.customer()
	  account = fake.customer_account(customer)
	  company = fake.Company() # note fake.company() creates a company name.


View the methods defined by DataProvider:

.. code:: bash

  $ pydoc3 data_bench_faker.DataProvider


.. |pypi| image:: https://img.shields.io/pypi/v/data-bench-faker.svg?style=flat-square&label=version
    :target: https://pypi.org/pypi/data-bench-faker
    :alt: Latest version released on PyPi

.. |python| image:: https://img.shields.io/pypi/pyversions/data-bench-faker.svg?style=flat-square
   :target: https://pypi.org/project/data-bench-faker/
   :alt: Python Versions	  

.. |license| image:: https://img.shields.io/badge/license-apache-blue.svg?style=flat-square
    :target: https://github.com/erikoshaughnessy/data-bench-faker/blob/master/LICENSE
    :alt: Apache license version 2.0  

.. _Faker: https://github.com/joke2k/faker

.. _Data Bench: https://github.com/Data-Bench/data-bench



