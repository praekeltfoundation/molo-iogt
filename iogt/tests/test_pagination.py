from django.test import TestCase, Client
from molo.core.tests.base import MoloTestCaseMixin

from molo.core.models import SiteLanguage


class RegistrationViewTest(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.client = Client()
        # Creates Main language
        self.english = SiteLanguage.objects.create(
            locale='en',
        )
        self.mk_main()

        # Creates a section under the index page
        self.english_section = self.mk_section(
            self.section_index, title='English section')
        for i in range(160):
            self.mk_article(
                self.english_section, title=str(i))

    def test_first_page_pagination(self):
        response = self.client.get('/sections/english-section/')

        self.assertNotContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=2" class="pagination__page">2</a>')
        self.assertContains(response, '<a href="?p=3" class="pagination__page">3</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15" class="pagination__page">15</a>')
        self.assertContains(response, '<a href="?p=16" class="pagination__page">16</a>')
        self.assertContains(response, 'Next')

    def test_second_page_pagination(self):
        response = self.client.get('/sections/english-section/?p=2')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1" class="pagination__page">1</a>')
        self.assertContains(response, '<a href="?p=3" class="pagination__page">3</a>')
        self.assertContains(response, '<a href="?p=4" class="pagination__page">4</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15" class="pagination__page">15</a>')
        self.assertContains(response, '<a href="?p=16" class="pagination__page">16</a>')
        self.assertContains(response, 'Next')

    def test_third_page_pagination(self):
        response = self.client.get('/sections/english-section/?p=3')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1" class="pagination__page">1</a>')
        self.assertContains(response, '<a href="?p=2" class="pagination__page">2</a>')
        self.assertContains(response, '<a href="?p=4" class="pagination__page">4</a>')
        self.assertContains(response, '<a href="?p=5" class="pagination__page">5</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15" class="pagination__page">15</a>')
        self.assertContains(response, '<a href="?p=16" class="pagination__page">16</a>')
        self.assertContains(response, 'Next')

    def test_fifth_page_pagination(self):
        response = self.client.get('/sections/english-section/?p=5')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1" class="pagination__page">1</a>')
        self.assertContains(response, '<a href="?p=2" class="pagination__page">2</a>')
        self.assertContains(response, '<a href="?p=3" class="pagination__page">3</a>')
        self.assertContains(response, '<a href="?p=4" class="pagination__page">4</a>')
        self.assertContains(response, '<a href="?p=6" class="pagination__page">6</a>')
        self.assertContains(response, '<a href="?p=7" class="pagination__page">7</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=15" class="pagination__page">15</a>')
        self.assertContains(response, '<a href="?p=16" class="pagination__page">16</a>')
        self.assertContains(response, 'Next')

    def test_fourteenth_page_pagination(self):
        response = self.client.get('/sections/english-section/?p=14')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1" class="pagination__page">1</a>')
        self.assertContains(response, '<a href="?p=2" class="pagination__page">2</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=12" class="pagination__page">12</a>')
        self.assertContains(response, '<a href="?p=13" class="pagination__page">13</a>')
        self.assertContains(response, '<a href="?p=15" class="pagination__page">15</a>')
        self.assertContains(response, '<a href="?p=16" class="pagination__page">16</a>')
        self.assertContains(response, 'Next')

    def test_fifteenth_page_pagination(self):
        response = self.client.get('/sections/english-section/?p=15')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1" class="pagination__page">1</a>')
        self.assertContains(response, '<a href="?p=2" class="pagination__page">2</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=13" class="pagination__page">13</a>')
        self.assertContains(response, '<a href="?p=14" class="pagination__page">14</a>')
        self.assertContains(response, '<a href="?p=16" class="pagination__page">16</a>')
        self.assertContains(response, 'Next')

    def test_sixteenth_page_pagination(self):
        response = self.client.get('/sections/english-section/?p=16')
        self.assertContains(response, 'Prev')
        self.assertContains(response, '<a href="?p=1" class="pagination__page">1</a>')
        self.assertContains(response, '<a href="?p=2" class="pagination__page">2</a>')
        self.assertContains(response, '...')
        self.assertContains(response, '<a href="?p=14" class="pagination__page">14</a>')
        self.assertContains(response, '<a href="?p=15" class="pagination__page">15</a>')
        self.assertNotContains(response, 'Next')
