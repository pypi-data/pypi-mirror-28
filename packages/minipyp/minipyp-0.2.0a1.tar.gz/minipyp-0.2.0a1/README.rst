#######
MiniPyP
#######
A more traditional web server in Python

.. image:: https://badge.fury.io/py/minipyp.svg
    :target: https://badge.fury.io/py/minipyp
    :alt: Release Status
.. image:: https://readthedocs.org/projects/minipyp/badge/?version=latest
    :target: http://minipyp.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://travis-ci.org/RyanGarber/minipyp.svg?branch=master
    :target: https://travis-ci.org/RyanGarber/minipyp
    :alt: Build Status

About the project
=================
MiniPyP (pronounced ``mini·pipe``) is an event-driven web server written in pure Python. **However, MiniPyP is not an application framework**. It's a full web server, with virtual hosts, reverse proxies, and everything else you need. MiniPyP is intended to replace Apache and nginx, so you can use Python without the performance hit of CGI.

MiniPyP has some more advanced features right out of the box, too. For example, when a user goes to ``/some/url`` on your server, and the directory's ``static`` option is set to False (default), the server will look for the file ``/some/url``. If it doesn't exist, but the file ``/some`` does, that file will be served. Extensions do not need to be specified with the ``static`` option set to False. In addition, if a file does not exist but a file named ``catchall`` exists, it will be served instead of a 404. This makes creating a single-page application that much more elegant.

Setup
=====
First, install MiniPyP via pip.

.. code-block:: bash

  pip install minipyp

To start a server within a Python program, specify a config like so (you may alternatively give a file location as the ``config``):

.. code-block:: python

  from minipyp import MiniPyP

  config = {
      'host': '0.0.0.0',
      'port': 80,
      'root': '/var/www/html',
      'timeout': 15,
      'error_pages': {
          404: {
              'html': '<p>The file <code>{uri}</code> could not be found.</p>'
          }
      }
  }

  MiniPyP(config=config).start()


You may also start a server via the command line. Unless specified, the config will be created and loaded from ``/etc/minipyp/minipyp.conf`` on Mac/Linux and ``%APPDATA%\MiniPyP\minipyp.conf`` on Windows.

.. code-block:: bash

  minipyp start [-c CONFIG]


Creating a page
===============

To create a page (e.g. 'https://mysite.com/test'), create a file called ``test.py`` in mysite.com's root with the following:

.. code-block:: python

  def render(server, request):
      return '<p>You requested the page <code>' + request.uri + '</code>.</p>'


Learn more
==========
See the full documentation at https://minipyp.readthedocs.io