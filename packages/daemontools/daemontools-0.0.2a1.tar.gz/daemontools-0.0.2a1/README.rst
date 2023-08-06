daemon-tools
============

Python modules for forking the application, single instance behavior, and sending logs over http POST.

These are the tools related to various daemon functionality, reused at various projects over time.
Daemonize is useful for dropping privileges after the resources have been acquired as root.
AppInstance does just that, provides information on whether the application is already started or not.
Tachyon Sender tracks the log file and sends it over HTTP POST. Today, Tachyon Sender could possibly be replaced
with generic applications, such as nxlog or Logstash. Tachyon Sender was written as a complement for Tachyon Application
written by `beli-sk <https://github.com/beli-sk>`_.

The project is licensed under LGPLv3.
