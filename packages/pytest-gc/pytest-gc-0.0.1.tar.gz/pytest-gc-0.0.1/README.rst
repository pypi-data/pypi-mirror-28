=========
pytest-gc
=========

.. image:: https://travis-ci.org/vtitor/pytest-gc.svg?branch=master
    :target: https://travis-ci.org/vtitor/pytest-gc

The garbage collector plugin for py.test.

Installation
------------
Install the plugin with::

    $ pip install pytest-gc

Usage
-----

There are a few options to use this plugin:

- Disable automatic garbage collection when running tests with ``gc-disable``.
- Set the garbage collection thresholds using ``gc-threshold`` option.
- Also, set the scope for the plugin's fixtures with ``gc-scope``, default ``function``.

So, for example, if you wanna change the gc thresholds for test run, just type::

    $ pytest --gc-threshold 5 7 8 --gc-scope session

Notes
-----

The repository of this plugin is at https://github.com/vtitor/pytest-gc.

For more info on py.test see http://pytest.org.
