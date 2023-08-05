.. default-role:: code

Keg: more than Flask
####################

.. image:: https://codecov.io/github/level12/keg/coverage.svg?branch=master
    :target: https://codecov.io/github/level12/keg?branch=master

.. image:: https://img.shields.io/pypi/v/Keg.svg
    :target: https://img.shields.io/pypi/v/Keg.svg

.. image:: https://img.shields.io/pypi/l/keg.svg
    :target: https://img.shields.io/pypi/l/keg.svg

.. image:: https://img.shields.io/pypi/pyversions/keg.svg
    :target: https://img.shields.io/pypi/pyversions/keg.svg

.. image:: https://img.shields.io/pypi/status/Keg.svg
    :target: https://img.shields.io/pypi/status/Keg.svg

.. image:: https://ci.appveyor.com/api/projects/status/wm35hheykxs8851r
    :alt: AppVeyor Build
    :target: https://ci.appveyor.com/project/level12/keg-6gnlh

Keg is an opinionated but flexible web framework built on Flask and SQLAlchemy.


Keg's Goal
==========

The goal for this project is to encapsulate Flask best practices and libraries so devs can avoid
boilerplate and work on the important stuff.

We will lean towards being opinionated on the big things (like SQLAlchemy as our ORM) while
supporting hooks and customizations as much as possible.

Think North of Flask but South of Django.

Features
========

Default Logging Configuration
-----------------------------

We highly recommend good logging practices and, as such, a Keg application does basic setup of the
Python logging system:

- Sets the log level on the root logger to INFO
- Creates two handlers and assigns them to the root logger:

  - outputs to stderr
  - outputs to syslog

- Provides an optional json formatter

The thinking behind that is:

- In development, a developer will see log messages on stdout and doesn't have to monitor a file.
- Log messages will be in syslog by default and available for review there if no other action is
  taken by the developer or sysadmin.  This avoids the need to manage log placement, permissions,
  rotation, etc.
- It's easy to configure syslog daemons to forward log messages to different files or remote log
  servers and it's better to handle that type of need at the syslog level than in the app.
- Structured log files (json) provide metadata details in a easy-to-parse format and should be
  easy to generate.
- The options and output should be easily configurable from the app to account for different needs
  in development and deployed scenarios.
- Keg's logging setup should be easy to turn off and/or completely override for situations where it
  hurts more than it helps.

Installation
============

`pip install keg`


App Configuration
=================

CLI Command
-----------

The command `<myapp> develop config` will give detailed information about the files and objects
being used to configure an application.

Profile Prority
---------------

All configuration classes with the name `DefaultProfile` will be applied to the app's config
first.

Then, the configuration classes that match the "selected" profile will be applied on top of the
app's existing configuration. This makes the settings from the "selected" profile override any
settings from the `DefaultProfile.`

Practically speaking, any configuration that applies to the entire app regardless of what context
it is being used in will generally go in `myapp.config` in the `DefaultProfile` class.

Selecting a Configuration Profile
---------------------------------

The "selected" profile is the name of the objects that the Keg configuration handling code will
look for.  It should be a string.

A Keg app considers the "selected" profile as follows:

    * If `config_profile` was passed into `myapp.init()` as an argument, use it as the
      selected profile.  The `--profile` cli option uses this method to set the selected profile and
      therefore has the highest priority.
    * Look in the app's environment namespace for "CONFIG_PROFILE".  If found, use it.
    * If running tests, use "TestProfile".  Whether or not the app is operating in this mode is
      controlled by the use of:

      - `myapp.init(use_test_profile=True)` which is used by `MyApp.testing_prep()`
      - looking in the app's environment namespace for "USE_TEST_PROFILE" which is used by
        `keg.testing.invoke_command()`

    * Look in the app's main config file (`app.config`) and all it's other
      config files for the variable `DEFAULT_PROFILE`.  If found, use the value from the file with
      highest priority.


Keg Development
===============

To develop on keg, begin by running our tests::

    git clone https://github.com/level12/keg keg-src
    cd keg-src
    cp keg_apps/db/user-config-tpl.py ~/.config/keg_apps.db/keg_apps.db-config.py
    # edit the DB connection info in this file (you don't have to use vim):
    vim ~/.config/keg_apps.db/keg_apps.db-config.py
    tox

You can then examine tox.ini for insights into our development process.  In particular, we:

* use `py.test` for testing (and coverage analysis)
* use `flake8` for linting

Preview Readme
--------------

When updating the readme, use `restview --long-description` to preview changes.


Issues & Discussion
====================

Please direct questions, comments, bugs, feature requests, etc. to:
https://github.com/level12/keg/issues

Current Status
==============

* Stable in a relatively small number of production environments.
* API is likely to change with smaller compatibility breaks happening more frequently than larger ones.



Changelog
=========

0.6.4 released 2018-01-09
-------------------------

- when testing, don't log to syslog by default (304a0a7_)

.. _304a0a7: https://github.com/level12/keg/commit/304a0a7


0.6.3 released 2018-01-09
-------------------------

- add '@cee:' prefix to json syslog formatter (b7ea5d3_)

.. _b7ea5d3: https://github.com/level12/keg/commit/b7ea5d3


0.6.2 released 2017-12-19
-------------------------

- db: get rid of code to replace session object (149b42c_)

.. _149b42c: https://github.com/level12/keg/commit/149b42c


0.6.1 released 2017-11-16
-------------------------

- fix quiet logging (e46fd2b_)
- a few small updates/fixes to readme (2044439_)

.. _e46fd2b: https://github.com/level12/keg/commit/e46fd2b
.. _2044439: https://github.com/level12/keg/commit/2044439


0.6.0 released 2017-08-18
-------------------------

- ADD: make CLIBase operate off `current_app` as last resort (1b358c1_)
- ADD: --quiet option to script options (6eb723f_)
- BREAKING CHANGE: adjust cli API on KegApp (af45880_)

.. _1b358c1: https://github.com/level12/keg/commit/1b358c1
.. _6eb723f: https://github.com/level12/keg/commit/6eb723f
.. _af45880: https://github.com/level12/keg/commit/af45880


0.5.1 released 2017-08-15
-------------------------

- ADD: mitigate CSRF bug in Flask-WTF (42a2e70_)
- ADD: config, init, and routing enhancements (cdfa901_)
- MAINT: upgrade to CircleCI 2.0 (60e3bfa_)

.. _42a2e70: https://github.com/level12/keg/commit/42a2e70
.. _cdfa901: https://github.com/level12/keg/commit/cdfa901
.. _60e3bfa: https://github.com/level12/keg/commit/60e3bfa


0.5.0 released 2017-06-27
-------------------------

- prep for pyp usage (23424b9_)
- Merge branch 'logging-improvements' (PR66_)

.. _23424b9: https://github.com/level12/keg/commit/23424b9
.. _PR66: https://github.com/level12/keg/pull/66



0.4.1 - 2017-02-09
------------------

* BUG: Properly quote pgsql identifiers during create (86852ad_)

.. _86852ad: https://github.com/level12/keg/commit/86852ad



0.4.0 - 2016-12-19
------------------

* BUG: Properly Update Keyring Config Data (7f1908f_)
* MSSQL dialect support (df7e89d_)
* MAINT: Refactor keyring to accept bytes (15bc04b_)
* MAINT: Remove deprecated flask hooks (4f7e2bf_)
* Remove unicode_literal futures (dc2fa85_)
* MAINT: Create windows build environment (983e040_)
* MAINT: Run CI with Docker (bc7a877_)
* Remove extra cp in readme (7e94815_)

.. _7f1908f: https://github.com/level12/keg/commit/7f1908f
.. _df7e89d: https://github.com/level12/keg/commit/df7e89d
.. _15bc04b: https://github.com/level12/keg/commit/15bc04b
.. _4f7e2bf: https://github.com/level12/keg/commit/4f7e2bf
.. _dc2fa85: https://github.com/level12/keg/commit/dc2fa85
.. _983e040: https://github.com/level12/keg/commit/983e040
.. _bc7a877: https://github.com/level12/keg/commit/bc7a877
.. _7e94815: https://github.com/level12/keg/commit/7e94815


