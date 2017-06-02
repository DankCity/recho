Reddit Echo
===========
Reposts Reddit posts from a target user to a specific slack channel

|PyPIVersion| |TravisCI| |CoverageStatus| |CodeHealth| |PythonVersions|

Helper class to make working with Selenium recho waits easier and
more accessible

.. |TravisCI| image:: https://travis-ci.org/DankCity/recho.svg?branch=master
    :target: https://travis-ci.org/DankCity/recho
.. |CoverageStatus| image:: https://coveralls.io/repos/github/DankCity/recho/badge.svg
   :target: https://coveralls.io/github/levi-rs/recho
.. |CodeHealth| image:: https://landscape.io/github/DankCity/recho/master/landscape.svg?style=flat
   :target: https://landscape.io/github/DankCity/recho/master
.. |PyPIVersion| image:: https://badge.fury.io/py/recho.svg
    :target: https://badge.fury.io/py/recho
.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/recho.svg
    :target: https://wiki.python.org/moin/Python2orPython3

(Optional) Create a virtual environment
=======================================
Its useful to create a virtual environment for installing and running recho

.. code-block:: bash

    $ sudo pip install virtualenv
    $ cd ~
    $ virtualenv .venvrecho
    $ source .venvrecho/bin/activate

Installation
============
Install from PyPI using pip:

.. code-block:: bash

    $ pip install --update recho

Add the configuration file

.. code-block:: bash

    $ touch ~/.recho.ini


Write the following into that file, adding your Slack token and channel

.. code-block:: bash

    [slack]
    # Follow instructions at https://my.slack.com/services/new/bot
    token: <Your slack token>
    channel: <your channel name>

Note that the channel name is without the hash.
`general` instead of `#general`

Running Recho
=============

Recho is designed for use with cron. Simply add an entry similar to the one below:

.. code-block:: bash

    $ sudo vi /etc/crontab

If you use a virtual environment:

.. code-block:: bash

     * * * * * user source ~/.venvrecho/bin/activate && recho acidtwist

Otherwise you can simply call recho directly

.. code-block:: bash

     * * * * * user recho acidtwist
