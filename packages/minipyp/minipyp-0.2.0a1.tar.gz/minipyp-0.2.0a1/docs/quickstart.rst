Quickstart
==========
There's a few ways to start a MiniPyP server.
The default config location is ``/etc/minipyp/minipyp.conf`` on Mac/Linux and ``%APPDATA%\MiniPyP\minipyp.conf`` on Windows.

In Code
-------
If no config parameter is given, the default location will be used.

.. code-block:: python

  from minipyp import MiniPyP

  MiniPyP(config='/path/to/config').start()

As a Daemon
-----------
Unlike above, if the config file does not exist, a default one will be generated.

.. code-block:: bash

  sudo minipyp start [-c CONFIG_PATH]