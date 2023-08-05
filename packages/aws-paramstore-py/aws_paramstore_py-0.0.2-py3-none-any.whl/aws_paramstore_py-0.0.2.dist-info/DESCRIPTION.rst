aws-paramstore-py
=================

Query params from AWS System Manager Parameter Store

Install
-------

.. code:: bash

    pip install aws-paramstore-py

Usage
-----

in console

.. code:: bash

    # AWS credentials from env vars
    aws-pspy /path/to/params
    # returns {"key1": "value1", "key2": "value2"}

in Python

.. code:: python

    import aws_paramstore_py as paramstore

    # AWS credentials from env vars
    params = paramstore.get('/path/to/params')
    # dict(key1: "value1", key2: "value2")


