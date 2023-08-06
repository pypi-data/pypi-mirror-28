===============================
url2markdown-cli
===============================

Fetch a url and translate it to markdown in one command.


Usage
-----

To install:

.. code-block:: bash

    $ pip install url2markdown-cli

To use:

.. code-block:: bash

    url2markdown --with-cache https://www.djangoproject.com/

To use your own custom url2markdown server instance (you should):

.. code-block:: bash

    export URL2MARKDOWN_URL='http://markdownplease.com/?url={url}'


Thanks
------

Thanks to @kennethreitz for his url2markdown project which this compliments:
    (https://github.com/kennethreitz/url2markdown)


History
=========

0.4.1 (2017-01-22)
---------------------

* Fixes README and HISTORY (oops)

0.4.0 (2017-01-22)
---------------------

* Update to use markdownplease.com
* Update requests-cache to be optional

0.2.1 (2015-01-11)
---------------------

* Updated readme to fix file path.

0.2.0 (2015-01-11)
---------------------

* Renamed module.

0.1.0 (2015-01-11)
---------------------

* First release on PyPI.


