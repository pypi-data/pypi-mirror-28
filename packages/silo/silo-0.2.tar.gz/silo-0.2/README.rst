Simply Logging
==============

Sometimes you just don't want to configure logging. Documentation_

Features
--------

- Configuration using ENV variables
- Low overhead debug operation (2 op codes)
- Audit functions to track business operations

Configuration
-------------

.. code:: shell

    export SILO_0=syslog_format:stderr
    export SILO_1=json_format:stderr
    export DEBUG=0

Examples
--------

.. code:: python

    from silo import info, debug, audit

    def hello(who='World'):
        info(f'Hello, {who}!')
        debug('done')

    hello()

    @audit
    def login(username, password):
        # do smart stuff here...
        return False

    login('duckie', 'secret')

This library is MIT licensed.

.. _Documentation: https://digitalmensch.github.io/silo/
