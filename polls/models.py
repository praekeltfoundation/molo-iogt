from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, FieldRowPanel)
from molo.core.models import ArticlePage, SectionPage, TranslatablePageMixin
from django.utils.translation import ugettext_lazy as _


SectionPage.subpage_types += ['polls.Question', 'polls.FreeTextQuestion']
ArticlePage.subpage_types += ['polls.Question', 'polls.FreeTextQuestion']


class PollsIndexPage(Page):
    parent_page_types = []
    subpage_types = ['polls.Question', 'polls.FreeTextQuestion']


class Question(TranslatablePageMixin, Page):
    subpage_types = ['polls.Choice']
    short_name = models.TextField(
        null=True, blank=True,
        help_text="The short name will replace the title when "
        "downloading your results. e.g 'How old are you' would be "
        "replaced by 'Age' in the title column.")
    extra_style_hints = models.TextField(
        default='',
        null=True, blank=True,
        help_text=_(
            "Styling options that can be applied to this section "
            "and all its descendants"))

    show_results = models.BooleanField(
        default=True,
        help_text=_("This option allows the users to see the results.")
    )
    randomise_options = models.BooleanField(
        default=False,
        help_text=_(
            "Randomising the options allows the options to be shown" +
            " in a different order each time the page is displayed."))
    result_as_percentage = models.BooleanField(
        default=True,
        help_text=_(
            "If not checked, the results will be shown as a total" +
            " instead of a percentage.")
    )
    allow_multiple_choice = models.BooleanField(
        default=False,
        help_text=_(
            "Allows the user to choose more than one option.")
    )
    content_panels = Page.content_panels + [FieldPanel('short_name')] + [
        MultiFieldPanel([
            FieldPanel('show_results'),
            FieldPanel('randomise_options'),
            FieldPanel('result_as_percentage'),
            FieldPanel('allow_multiple_choice')], heading=_(
                "Question Settings",))]

    def user_choice(self, user):
        return ChoiceVote.objects.get(
            user=user, question__id=self.id).choice

    def can_vote(self, user):
        return not (ChoiceVote.objects.filter(
            user=user, question__id=self.get_main_language_page().id).exists())

    def choices(self):
        if self.randomise_options:
            return Choice.objects.live().child_of(self).order_by('?')
        else:
            return Choice.objects.live().child_of(self)

    def get_effective_extra_style_hints(self):
        parent_section = SectionPage.objects.all().ancestor_of(self).last()
        if parent_section:
            return self.extra_style_hints or \
                parent_section.get_effective_extra_style_hints()
        else:
            parent_article = ArticlePage.objects.all().ancestor_of(self).last()
            if parent_article:
                return self.extra_style_hints or \
                    parent_article  .get_effective_extra_style_hints()
        return self.extra_style_hints

Question.settings_panels = [
    MultiFieldPanel(
        [FieldRowPanel(
            [FieldPanel('extra_style_hints')], classname="label-above")],
        "Meta")
]


class FreeTextQuestion(Question):
    subpage_types = []
    content_panels = Page.content_panels
    numerical = models.BooleanField(
        default=False,
        help_text=_(
            "When selected, this question will allow numerical data only")
    )
    content_panels = Page.content_panels + [MultiFieldPanel([
        FieldPanel('numerical')], heading=_("Question Settings",))]

    def __init__(self, *args, **kwargs):
        super(FreeTextQuestion, self).__init__(*args, **kwargs)
        self.show_results = False

    def can_vote(self, user):
        return not (FreeTextVote.objects.filter(
            user=user, question__id=self.get_main_language_page().id).exists())


class Choice(TranslatablePageMixin, Page):
    subpage_types = []
    votes = models.IntegerField(default=0)
    choice_votes = models.ManyToManyField('ChoiceVote',
                                          related_name='choices',
                                          blank=True)
    short_name = models.TextField(
        null=True, blank=True,
        help_text="The short name will replace the title when "
        "downloading your results. e.g '10 years old' would be "
        "replaced by '10' in the title column.")

    promote_panels = Page.promote_panels + [FieldPanel('short_name')] + [
        FieldPanel('votes'),
    ]


class ChoiceVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='choice_votes')
    choice = models.ManyToManyField('Choice', blank=True)
    question = models.ForeignKey('Question')
    submission_date = models.DateField(null=True, blank=True,
                                       auto_now_add=True)

    @property
    def answer(self):
        return ','.join([c.short_name or c.title for c in self.choice.all()])


class FreeTextVote(models.Model):
    user = models.ForeignKey('auth.User', related_name='text_votes')
    question = models.ForeignKey('FreeTextQuestion')
    answer = models.TextField(blank=True, null=True)
    submission_date = models.DateField(null=True, blank=True,
                                       auto_now_add=True)
