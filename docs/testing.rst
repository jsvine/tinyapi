=======
Testing
=======

Here's how to run TinyAPI's tests:

Install the testing dependencies
--------------------------------

.. code-block:: sh

    pip install nose
    pip install coverage

Tell TinyAPI which account to use
---------------------------------

.. code-block:: sh

    export TINYAPI_TEST_USERNAME="tinyapi-test-account"
    export TINYAPI_TEST_PASSWORD="XXXXXXXX"

Run the tests
-------------

.. code-block:: sh

    nosetests --with-coverage --cover-erase -cover-package tinyapi
