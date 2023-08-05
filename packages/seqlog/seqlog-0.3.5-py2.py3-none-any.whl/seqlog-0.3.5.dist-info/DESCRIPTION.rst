===============================
SeqLog
===============================


.. image:: https://img.shields.io/pypi/v/seqlog.svg
        :target: https://pypi.python.org/pypi/seqlog

.. image:: https://img.shields.io/travis/tintoy/seqlog.svg
        :target: https://travis-ci.org/tintoy/seqlog

.. image:: https://readthedocs.org/projects/seqlog/badge/?version=latest
        :target: https://seqlog.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


SeqLog enables logging from Python to `Seq <https://getseq.net/>`_.

It also adds support for logging with named format arguments (via keyword arguments) in the same way ``"{arg1}".format(arg1="foo")`` does.

* Free software: MIT license
* Documentation: https://seqlog.readthedocs.io.


=======
History
=======

0.3.4 (2017-11-27)
------------------

* Fix sample code (#2).

0.3.3 (2016-11-18)
------------------

* Use streaming mode when posting to Seq (#1)

0.3.2 (2016-11-18)
------------------

* Updated release notes

0.3.1 (2016-11-18)
------------------

* Further work relating to intermittent "RuntimeError: The content for this response was already consumed" when publishing log entries (#1)

0.3.0 (2016-11-16)
------------------

* Fix for intermittent "RuntimeError: The content for this response was already consumed" when publishing log entries (#1)

0.2.0 (2016-07-09)
------------------

* Support for configuring additional log handlers when calling log_to_seq.
* Support for global log properties (statically-configured properties that are added to all outgoing log entries).

0.0.1 (2016-07-07)
------------------

* First release on PyPI.

0.0.7 (2016-07-09)
------------------

* ``log_to_seq`` now returns the SeqLogHandler to enable forced flushing of log records to Seq.
* Change ``auto_flush_timeout`` to a ``float`` representing seconds (instead of milliseconds).
* Update ``testharness.py`` to actually log to Seq.
  You can override the server URL and API key using the ``SEQ_SERVER_URL`` and ``SEQ_API_KEY`` environment variables.
* Update usage information in documentation.
* Python 3 only for now (sorry, but logging in Python 2 doesn't have all the required extensibility points). If the need to support Python 2 becomes great enough then I'll try to find a way.

0.1.0 (2016-07-09)
------------------

* Proper versioning starts today :)



