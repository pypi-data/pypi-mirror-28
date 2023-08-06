============================================
Mill: A Python Client for Textile's REST API
============================================

.. image:: https://gitlab.com/weareset/mill-py/badges/master/pipeline.svg
    :target: https://gitlab.com/weareset/mill-py/badges/master/pipeline.svg
.. image:: https://gitlab.com/weareset/mill-py/badges/master/coverage.svg
    :target: https://gitlab.com/weareset/mill-py/badges/master/coverage.svg

Mill is the official, lightweight Python client for interacting with Textile's REST API.

.. _installation:

Installation
============

Mill is supported on Python 2.7, 3.3, 3.4, 3.5 and 3.6. The recommended way to install Mill is via
`pip <https://pypi.python.org/pypi/pip>`_.

.. code-block:: bash

  pip install mill

To install the latest development version of Mill run the following instead:

.. code-block:: bash

  pip install --upgrade git+git://gitlab.com/textileio/mill-py.git

For instructions on installing Python and pip see "The Hitchhiker's Guide to Python" `Installation Guides
<http://docs.python-guide.org/en/latest/starting/installation/>`_.

.. _quick_start:

Quickstart
==========

Authentication
--------------

Textile's REST API uses scoped `JSON Web Tokens (JWT) <https://jwt.io/>`_ to authenticate with external clients.
For example, whenever a request is made by the Mill Python client, one of these tokens is passed along via
`HTTP Basic Auth <https://en.wikipedia.org/wiki/Basic_access_authentication>`_, identifying the requester and stating
what specific permissions they have.

.. note:: We take your users' privacy very seriously. So, with the exception of registering your client, communications
   between the Mill client and Textile's REST API are authenticated with user-scoped tokens.

In order to use the Mill Python client, you'll need to pass a ```client_id``` and ```client_secret``` pair to the Mill
``Client`` object. These are only used to register your client, at which point they'll be exchanged for scoped tokens
which are used internally by the Mill ``Client``. Please check out Textile's
`documentation <http://docs.textile.io/overview/accounts-security/>`_ to learn how to create an account and get your
client credentials.

Once you have your credentials in hand, instantiation, authenticating, and interacting with the Mill ``Client`` is
straightforward:

.. code-block:: python

  from datetime import datetime, timedelta
  from mill import Client
  client = Client(client_id="uuid",
                  client_secret="shhh",
                  bundle="com.bundle.id",
                  api_url="https://api.textile.io")

With the ``client`` instance you can now interact with Textile's REST API:

.. code-block:: python

  # Get health of the api endpoint
  client.get_health()
  # Request all features for the given app (default for the past day)
  ndjson = client.request_features()
  # Alternatively, you can specify specific query parameters
  ndjson = client.request_features(lookback=timedelta(days=2))
  # Should be equivalent to the above query
  ndjson = client.request_features(start=datetime.now() - timedelta(days=2))
  # Ignore everything in the last day
  ndjson = client.request_features(start=datetime.now() - timedelta(days=2),
                                   end=datetime.now() - timedelta(days=1))
  # Query for a specific feature type, which can include any/all of:
  # ["system", "states", "events", "arrivals", "departures", "places", "trips", "tags", "cycles", "models"]
  ndjson = client.request_features(types=["arrivals", "departures"])

The above queries all return a generator over the features (so the calls will return almost instantly). You can then
iterate over the features, convert them to a list, etc. For large requests, you can also stream the features directly
to a file using the `ndjson <http://ndjson.org>`_ format:

.. code-block:: python

  # This method also takes all the same query parameters as `request_features`
  params = {...}
  client.download_features("output.ndjson", **params)
  # Alternatively, you can specify your own file-like object to write to
  with open("output.ndjson", "w+") as f:  # remember to use `with` to automatically close and flush files
      client.download_features(f)

Mill then makes it easy to work with your preferred SciPy libraries and tools:

.. code-block:: python

  # Import pandas or other data science libraries
  import pandas as pd
  df = (pd.DataFrame
        .from_records(client.request_features())
        .assign(timestamp=lambda x: pd.to_datetime(x.timestamp))
        .set_index("timestamp")
        .sort_index()
        )
  df.head()
  #                          application_id  application_is_active  application_is_backgrounded  application_is_inactive
  # timestamp
  # 2018-01-15 18:54:47.768              id                   True                        False                    False
  # 2018-01-15 19:05:41.822              id                  False                        False                     True
  # 2018-01-15 19:06:38.552              id                  False                        False                     True
  # 2018-01-15 19:06:40.109              id                  False                        False                     True
  # 2018-01-15 19:07:28.885              id                  False                        False                     True

.. _support:

Discussion and Support
======================

Real-time chat can be conducted via Textile's `developer slack channel <https://textile-public.slack.com>`_.

Please file bugs and feature requests as issues on ... after first searching to
ensure a similar issue was not already filed. If such an issue already exists
please give it a thumbs up reaction. Comments to issues containing additional
information are certainly welcome.

.. note:: This project is released with a `Contributor Code of Conduct
   <./CODE_OF_CONDUCT.md>`_. By participating in this project you agree to abide by its terms.

Documentation
=============

Please see Mill's `documentation <http://docs.textile.io/clients/python/>`_ for more examples of what you can do
with Mill.
