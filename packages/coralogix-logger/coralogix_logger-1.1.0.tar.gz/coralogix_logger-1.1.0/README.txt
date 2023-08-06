.. image:: http://res.cloudinary.com/coralogix/image/upload/v1482035757/logos_yjmwij.png

==================
Table of contents
==================
""""""""""
- Install
""""""""""
""""""""""
- General
""""""""""
"""""""""""""""""""""
- Python integration
"""""""""""""""""""""
""""""""""
- uWSGI
""""""""""


=========
Install
=========


.. code:: sh

    $ pip install coralogix_logger

=========
General
=========

    **PRIVATE KEY** - A unique ID which represents your company. This ID will be sent to your mail once you register to Coralogix.

    **APPLICATION NAME** - The name of your main application. For example, a company named “SuperData” would probably insert the “SuperData” string parameter; or if they want to debug their test environment, they might insert the “SuperData – Test”.

    **SUBSYSTEM NAME** - Your application probably has multiple subsystems. For example: Backend servers, Middleware, Frontend servers etc. In order to help you examine the data you need, inserting the subsystem parameter is vital.

======================
Python integration
======================

.. code:: python

    import logging
    from coralogix.coralogix_logger import CoralogixLogger

    PRIVATE_KEY = "[YOUR_PRIVATE_KEY_HERE]"
    APP_NAME = "[YOUR_APPLICATION_NAME]"
    SUB_SYSTEM = "[YOUR_SUBSYTEM_NAME]"

    # Get an instance of Python standard logger.
    logger = logging.getLogger("Python Logger")

    # Get a new instance of Coralogix logger.
    coralogix_handler = CoralogixLogger(PRIVATE_KEY, APP_NAME, SUB_SYSTEM)

    # Add coralogix logger as a handler to the standard Python logger.
    logger.addHandler(coralogix_handler)

    # Send message
    logger.info("Hello World!")


===========================
Configuration Under uWSGI
===========================

- **By default uWSGI does not enable threading support within the Python interpreter core. This means it is not possible to create background threads from Python code. As the Coralogix logger relies on being able to create background threads (for sending logs), this option is required.**

You can enable threading either by passing **--enable-threads** to uWSGI command line:

.. code:: sh

    $ uwsgi wsgi.ini --enable-threads

Another option is to enable threads in your wsgi.ini file:

    **wsgi.ini:**

.. code:: python

    ...
    enable-threads = true
    ...


- **If you are using multiple processes/workers and you don't use "lazy-apps = true" then you must wait for the process to finish the fork before you can send logs with Coralogix logger. You can configure the logger during initialization process, but you must wait for the fork to complete before you can actually send your logs. You can use uWSGI @postfork decorator to be sure when it's safe to use Coralogx logger:**


.. code:: python

    import uwsgi
    from uwsgidecorators import *

    @postfork
    def on_worker_ready():
        #It is now safe to send logs with Coralogix logger
