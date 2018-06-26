from django.test import TestCase, Client

from molo.core.models import (
    Main, Languages, SiteLanguageRelation, SiteLanguage)
from molo.core.tests.base import MoloTestCaseMixin


class RegistrationViewTest(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.client = Client()
        # Creates Main language
        self.mk_main()
        main = Main.objects.all().first()
        self.english = SiteLanguageRelation.objects.create(
            language_setting=Languages.for_site(main.get_site()),
            locale='en',
            is_active=True)

        # Creates a section under the index page
        self.english_section = self.mk_section(
            self.section_index, title='English section')
        for i in range(160):
            self.mk_article(
                self.english_section, title=str(i))

    def test_first_page_pagination(self):
        response = self.client.get('/sections-main-1/english-section/')
        self.assertNotContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=2">2</a>')
        self.assertContains(response, '<a href="?p=3">3</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15">15</a>')
        self.assertContains(response, '<a href="?p=16">16</a>')
        self.assertContains(response, 'Next')

    def test_second_page_pagination(self):
        response = self.client.get('/sections-main-1/english-section/?p=2')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1">1</a>')
        self.assertContains(response, '<a href="?p=3">3</a>')
        self.assertContains(response, '<a href="?p=4">4</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15">15</a>')
        self.assertContains(response, '<a href="?p=16">16</a>')
        self.assertContains(response, 'Next')

    def test_third_page_pagination(self):
        response = self.client.get('/sections-main-1/english-section/?p=3')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1">1</a>')
        self.assertContains(response, '<a href="?p=2">2</a>')
        self.assertContains(response, '<a href="?p=4">4</a>')
        self.assertContains(response, '<a href="?p=5">5</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15">15</a>')
        self.assertContains(response, '<a href="?p=16">16</a>')
        self.assertContains(response, 'Next')

    def test_fifth_page_pagination(self):
        response = self.client.get('/sections-main-1/english-section/?p=5')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1">1</a>')
        self.assertContains(response, '<a href="?p=2">2</a>')
        self.assertContains(response, '<a href="?p=3">3</a>')
        self.assertContains(response, '<a href="?p=4">4</a>')
        self.assertContains(response, '<a href="?p=6">6</a>')
        self.assertContains(response, '<a href="?p=7">7</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15">15</a>')
        self.assertContains(response, '<a href="?p=16">16</a>')
        self.assertContains(response, 'Next')

    def test_fourteenth_page_pagination(self):
        response = self.client.get('/sections-main-1/english-section/?p=14')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1">1</a>')
        self.assertContains(response, '<a href="?p=2">2</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=12">12</a>')
        self.assertContains(response, '<a href="?p=13">13</a>')
        self.assertContains(response, '<a href="?p=15">15</a>')
        self.assertContains(response, '<a href="?p=16">16</a>')
        self.assertContains(response, 'Next')

    def test_fifteenth_page_pagination(self):
        response = self.client.get('/sections-main-1/english-section/?p=15')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1">1</a>')
        self.assertContains(response, '<a href="?p=2">2</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=13">13</a>')
        self.assertContains(response, '<a href="?p=14">14</a>')
        self.assertContains(response, '<a href="?p=16">16</a>')
        self.assertContains(response, 'Next')

    def test_sixteenth_page_pagination(self):
        response = self.client.get('/sections-main-1/english-section/?p=16')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1">1</a>')
        self.assertContains(response, '<a href="?p=2">2</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=14">14</a>')
        self.assertContains(response, '<a href="?p=15">15</a>')
        self.assertNotContains(response, 'Next')
