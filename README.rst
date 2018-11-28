iogt
=========================

This is an application scaffold for Molo_.

Getting started
---------------

To get started::

    $ virtualenv ve
    $ pip install -r requirements.txt
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

Writing Test Cases
==================

You can make use of the Molo test mixin `molo.core.tests.base.MoloTestCaseMixin`

* The Molo test mixin contains helper methods to generate test content necessary for the main sight.

::

    class MyTest(MoloTestCaseMixin, TestCase):

        def setUp(self):
            self.mk_main()
            main = Main.objects.all().first()
            lang = Languages.for_site(main.get_site()
            self.english = SiteLanguageRelation.objects.create(
                language_setting=lang), locale='en', is_active=True)

            self.user = User.objects.create_user(
                'test', 'test@example.org', 'test')

            self.client = Client()
            ...

        def test_register_auto_login(self):
            # Not logged in, redirects to login page
            login_url = reverse('molo.profiles:edit_my_profile')
            expected_url = '/login/?next=/profiles/edit/myprofile/'

            response = self.client.get(login_url)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['Location'], expected_url)

IoGT Middlewares
================

`SSLRedirectMiddleware`

`FaceBookPixelHistoryCounter`

`IogtMoloGoogleAnalyticsMiddleware`


Enabled Molo Plugins
====================

* `molo.profiles` (within molo core) https://github.com/praekelt/molo
* `molo.usermetadata` https://github.com/praekelt/molo.usermetadata
* `molo.surveys` https://github.com/praekelt/molo.surveys
* `molo.commenting` https://github.com/praekelt/molo.commenting
* `molo.polls` https://github.com/praekelt/molo.polls


Basic Settings and their defaults
=================================

    for all available settings see

    `./iogt/settings/base.py`, `./iogt/settings/dev.py`, `./iogt/settings/docker.py` and `./iogt/settings/production.py`

::

    ADMIN_LANGUAGE_CODE = 'en'

    AWS_STORAGE_BUCKET_NAME = ''
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    FACEBOOK_PIXEL = <FACEBOOK_PIXEL KEY>
    FACEBOOK_PIXEL_COOKIE_KEY = 'facebook_pixel_hit_count'

    MAINTENANCE_MODE = None
    MAINTENANCE_MODE_TEMPLATE = 'maintenance.html'

    FROM_EMAIL = 'support@moloproject.org'
    CONTENT_IMPORT_SUBJECT = 'Molo Content Import'
