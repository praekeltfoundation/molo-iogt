from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from molo.core.models import SiteLanguage, SectionPage
from molo.core.tests.base import MoloTestCaseMixin

from molo.polls.models import Choice, Question, ChoiceVote, PollsIndexPage


class ModelsTestCase(MoloTestCaseMixin, TestCase):

    def setUp(self):
        self.user = self.login()
        self.mk_main()
        # Creates Main language
        self.english = SiteLanguage.objects.create(locale='en')
        # Create polls index page
        self.polls_index = PollsIndexPage(title='Polls', slug='polls')
        self.main.add_child(instance=self.polls_index)
        self.polls_index.save_revision().publish()

    def test_section_page_question(self):
        section = SectionPage(
            title='section', slug='section', extra_style_hints='purple')
        self.main.add_child(instance=section)
        section.save_revision().publish()

        question = Question(title='is this a test')
        section.add_child(instance=question)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'section')
        response = self.client.get(
            '/section/')
        self.assertContains(response, "is this a test")
        self.assertEquals(section.get_effective_extra_style_hints(), 'purple')
        self.assertEquals(question.get_effective_extra_style_hints(), 'purple')

    def test_poll_vote(self):
        # make choices
        choice1 = Choice(title='yes')
        # make a question
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')
        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        vote_count = ChoiceVote.objects.all()[0].choice.all()[0].votes
        self.assertEquals(vote_count, 1)

    def test_question_choices(self):
        choice1 = Choice(title='yes')
        choice2 = Choice(title='no')
        choice3 = Choice(title='maybe')
        choice4 = Choice(title='definitely')
        choice5 = Choice(title='idk')

        question = Question(title='is this a test', randomise_options=True)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.add_child(instance=choice3)
        question.add_child(instance=choice4)
        question.add_child(instance=choice5)

        choices = question.choices()
        self.assertEqual(choices.get(title='yes'), choice1)
        self.assertEqual(choices.get(title='no'), choice2)
        self.assertEqual(choices.get(title='maybe'), choice3)
        self.assertEqual(choices.get(title='definitely'), choice4)
        self.assertEqual(choices.get(title='idk'), choice5)

        question.randomise_options = False
        choices = question.choices()
        self.assertEqual(choices.all().first(), choice1)
        self.assertEqual(choices.all().last(), choice5)
