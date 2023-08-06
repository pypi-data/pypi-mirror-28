Configuring MiniPyP
===================
MiniPyP uses YAML for its configuration.

When passing a dict as the config, convert all keys like so: "MIME Types" -> "mime_types".

Example Config
--------------

.. code-block:: yaml

  Host: 0.0.0.0
  Port: 80
  Root: /var/www/default
  Timeout: 15
  Sites:
  - URIs:
    - mysite.com
    - www.mysite.com
    Root: /var/www/mysite
    Paths:
      "/tunnel":
        Proxy: http://127.0.0.1:8080
  Directories:
    "/":
      Public: false
    "/var/www":
      Public: true

Basics
------
These options are required to start the server. They are all you need to get started, but are very limited.

=======  ===========
Name     Description
=======  ===========
Host     Host to listen on, use "0.0.0.0" to allow all
Port     Port to listen on
Root     Default document root
Timeout  Keep-Alive timeout in seconds, default 15
=======  ===========

Sites
-----
You can configure different sites by hostname.

=====  ========  ===========
Name   Required  Description
=====  ========  ===========
URIs   Yes       List of hostnames this site applies to
Root   No        Document root for this site
Paths  No        Path options (see `Paths`_ below)
=====  ========  ===========

Directories
-----------
You can specify options for any directory on the server.
The directory path can be a string or a regular expression.

=============  ===========
Name           Description
=============  ===========
Public         If false, trying to view this directory will give a 403
Static         If true, the server will not use catchall files or allow extensions to be omitted
Indexing       If false, the server will not give a list of files in the directory
Don't Handle   List of filetypes to serve as-is without running them
Allow Options  List of options to allow the user to override with .minipyp.yml (not yet implemented)
=============  ===========

Paths
-----
You can specify options for any request path globally or inside a Site.
The path can be a string or a regular expression.

=====  ===========
Name   Description
=====  ===========
Proxy  URL to serve as a reverse-proxy
=====  ===========

Error Pages
-----------
You can specify custom error pages globally or inside a Directory.
You should provide one of the following options.

====  ===========
Name  Description
====  ===========
HTML  Pre-made HTML to serve, {uri} will be replaced with the request URI
File  File to serve, e.g. '/var/www/errors/404.py'
====  ===========