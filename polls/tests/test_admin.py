import datetime

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import SiteLanguage

from molo.polls.admin import QuestionAdmin, download_as_csv
from molo.polls.models import (Choice, Question, FreeTextQuestion,
                               PollsIndexPage)


class ModelsTestCase(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.user = self.login()
        self.mk_main()
        # Creates Main language
        self.english = SiteLanguage.objects.create(locale='en')
        # Create polls index page
        self.polls_index = PollsIndexPage(title='Polls', slug='polls')
        self.main.add_child(instance=self.polls_index)
        self.polls_index.save_revision().publish()

    def test_download_csv_question(self):
        # make choices
        choice1 = Choice(title='yes')
        choice2 = Choice(title='no')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',superuser,'
                           '"yes,no"\r\n')
        self.assertEquals(str(response), expected_output)

    def test_choice_short_name(self):
        # make choices
        choice1 = Choice(title='yes', short_name='y')
        choice2 = Choice(title='no', short_name='n')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',superuser,'
                           '"y,n"\r\n')
        self.assertEquals(str(response), expected_output)

    def test_choice_short_name_single_choice(self):
        # make choices
        choice1 = Choice(title='yes', short_name='y')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',superuser,'
                           'y\r\n')
        self.assertEquals(str(response), expected_output)

    def test_download_csv_free_text_question(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': 'this is an answer'})
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',superuser,'
                           'this is an answer\r\n')
        self.assertEquals(str(response), expected_output)

    def test_download_csv_free_text_question_short_name(self):
        question = FreeTextQuestion(
            title='is this a test', short_name='short')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': 'this is an answer'})
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nshort,' + date + ',superuser,'
                           'this is an answer\r\n')
        self.assertEquals(str(response), expected_output)
