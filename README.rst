iogt
=========================

This is an application scaffold for Molo_.

Getting started
---------------

To get started::

    $ virtualenv ve
    $ pip install -r requirements.txt.
    $ pip install -e .
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver

You can now connect access the demo site on http://localhost:8000
On http://localhost:8000/admin/ add a Site Language


.. _Molo: https://molo.readthedocs.org

Building SCSS Files
=====================
The project makes use of gulp to minify JavaScript and css
::

$ sudo apt-get install nodejs
$ npm install -g gulp
$ gulp styles


Running Workers
===============

* Celery for async tasks
* Celery Beat for running tasks every minute

::

$ ./manage.py celery worker -A iogt -l INFO
$ ./manage.py celerybeat -A iogt -l INFO
$ sudo service redis-server start


Testing
=======
The molo stack currently utilises pytest unit testing library.
The config file can be located on the project root `setup.cfg`
Test coverage enabled to out put the coverage results on the terminal by default.

The django test settings are also found on the root of the project files
namely `test_settings.py`

Installing test requirements and running the tests::


$ pip install -r requirements-dev.txt
$ flake8
$ py.test


Enabled Molo Plugins
====================

* `molo.profiles` (within molo core) https://github.com/praekelt/molo
* `molo.usermetadata` https://github.com/praekelt/molo.usermetadata
* `molo.surveys` https://github.com/praekelt/molo.surveys
* `molo.commenting` https://github.com/praekelt/molo.commenting
* `molo.polls` https://github.com/praekelt/molo.polls
