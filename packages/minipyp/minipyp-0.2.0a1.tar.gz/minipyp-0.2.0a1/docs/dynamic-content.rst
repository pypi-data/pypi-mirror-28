Dynamic Content
===============
You may use Handlers to serve any type of dynamic content, but only a Python handler is provided by default.

Here's an example index.py that displays the client's IP and the current date.

.. code-block:: python

  from datetime.datetime import now

  def render(server, request):
      return 'Your IP: ' + server.peer[0] + '\nCurrent date: ' + str(now())


Server object:

=========  ===========
Attribute  Description
=========  ===========
peer       Client info, e.g. ['127.0.0.1', 25565]
=========  ===========


Request object:

============  ===========
Attribute     Description
============  ===========
protocol      Protocol version, e.g. "HTTP/1.1"
scheme        HTTP scheme, e.g. "https"
method        HTTP method, e.g. "POST"
headers       Request headers, e.g. {'User-Agent': 'Client/1.0'} (case-insensitive)
host          Request hostname, e.g. "mysite.com"
path          Request path, e.g. "/file.txt"
uri           Full request path, e.g. "/file.txt?query=string"
query_string  Query string, e.g. "query=string"
query         Parsed query string, e.g. {'query': ['string']}
body          Request body (ASCII)
post          Parsed request body, e.g. {'post': ['param']}
site          Site config, e.g. {'uris': ['mysite.com', 'www.mysite.com'], ...}
root          Document root as given in config
file          Absolute path of requested file (document root + request path)
============  ===========