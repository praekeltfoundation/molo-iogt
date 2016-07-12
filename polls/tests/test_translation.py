from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from molo.core.models import SiteLanguage
from molo.core.tests.base import MoloTestCaseMixin

from molo.polls.models import (Choice, Question, FreeTextQuestion,
                               FreeTextVote, ChoiceVote, PollsIndexPage)


class ModelsTestCase(MoloTestCaseMixin, TestCase):

    def setUp(self):
        self.user = self.login()
        self.mk_main()
        # Creates Main language
        self.english = SiteLanguage.objects.create(locale='en')
        # Creates Child language
        self.french = SiteLanguage.objects.create(locale='fr')
        # Create polls index page
        self.polls_index = PollsIndexPage(title='Polls', slug='polls')
        self.main.add_child(instance=self.polls_index)
        self.polls_index.save_revision().publish()

    def test_translated_question_exists(self):
        client = Client()
        client.login(username='superuser', password='pass')

        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))
        page = Question.objects.get(
            slug='french-translation-of-is-this-a-test')
        page.save_revision().publish()

        response = self.client.get(reverse(
            'wagtailadmin_explore', args=[self.polls_index.id]))
        self.assertContains(response,
                            '<a href="/admin/pages/%s/edit/"'
                            % page.id)

    def test_translated_choice_exists(self):
        client = Client()
        client.login(username='superuser', password='pass')

        choice1 = Choice(title='yes')
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[choice1.id, 'fr']))
        page = Choice.objects.get(
            slug='french-translation-of-yes')
        page.save_revision().publish()

        response = self.client.get(reverse(
            'wagtailadmin_explore', args=[question.id]))

        self.assertContains(response,
                            '<a href="/admin/pages/%s/edit/"'
                            % page.id)

    def test_votes_stored_against_main_language_question(self):
        client = Client()
        client.login(username='superuser', password='pass')

        choice1 = Choice(title='yes')
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[choice1.id, 'fr']))
        page = Choice.objects.get(
            slug='french-translation-of-yes')
        page.save_revision().publish()

        client.post(reverse('molo.polls:vote',
                            kwargs={'question_id': question.id}),
                    {'choice': choice1.id})

        vote = ChoiceVote.objects.all().first()
        self.assertEqual(vote.choice.all().first().id, choice1.id)

    def test_user_not_allow_to_vote_in_other_languages_once_voted(self):
        client = Client()
        client.login(username='superuser', password='pass')

        choice1 = Choice(title='yes')
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[choice1.id, 'fr']))
        page = Choice.objects.get(
            slug='french-translation-of-yes')
        page.save_revision().publish()

        client.post(reverse('molo.polls:vote',
                            kwargs={'question_id': question.id}),
                    {'choice': choice1.id})

        response = self.client.get('/')
        self.assertContains(response, 'Show Results')

        response = self.client.get('/locale/fr/')
        response = self.client.get('/')
        self.assertContains(response, 'Show Results')

    def test_translated_free_text_question_exists(self):
        client = Client()
        client.login(username='superuser', password='pass')
        question = FreeTextQuestion(title='what is this')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))

        page = FreeTextQuestion.objects.get(
            slug='french-translation-of-what-is-this')
        page.save_revision().publish()

        response = self.client.get(reverse(
            'wagtailadmin_explore', args=[self.polls_index.id]))

        self.assertContains(response,
                            '<a href="/admin/pages/%s/edit/"'
                            % page.id)

    def test_free_text_question_reply_stored_against_main_language(self):
        client = Client()
        client.login(username='superuser', password='pass')
        question = FreeTextQuestion(title='what is this')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))

        page = FreeTextQuestion.objects.get(
            slug='french-translation-of-what-is-this')
        page.save_revision().publish()

        client.post(reverse(
            'molo.polls:free_text_vote',
            kwargs={'question_id': page.id}),
            {'answer': 'A test free text question '})
        answer = FreeTextVote.objects.all().first()
        self.assertEquals(answer.question.id, question.id)
