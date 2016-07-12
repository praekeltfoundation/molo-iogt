
from copy import copy

from django import template

from molo.polls.models import Question, Choice, PollsIndexPage

register = template.Library()


@register.inclusion_tag('polls/poll_page.html',
                        takes_context=True)
def poll_page(context, pk=None):
    context = copy(context)
    locale_code = context.get('locale_code')
    page = PollsIndexPage.objects.live().first()
    if page:
        questions = (
            Question.objects.live().child_of(page).filter(
                languages__language__is_main_language=True).specific())
    else:
        questions = []

    context.update({
        'questions': [
            a.get_translation_for(locale_code) or a for a in questions]
    })
    return context


@register.inclusion_tag('polls/poll_page_in_section.html',
                        takes_context=True)
def poll_page_in_section(context, pk=None, page=None):
    context = copy(context)
    locale_code = context.get('locale_code')
    if page:
        questions = (
            Question.objects.live().child_of(page).filter(
                languages__language__is_main_language=True).specific())
    else:
        questions = []

    context.update({
        'questions': [
            a.get_translation_for(locale_code) or a for a in questions]
    })
    return context


@register.assignment_tag(takes_context=True)
def load_choices_for_poll_page(context, question):
    page = question.get_main_language_page()
    locale = context.get('locale_code')
    qs = Choice.objects.live().child_of(page).filter(
        languages__language__is_main_language=True)

    if not locale:
        return qs

    return [a.get_translation_for(locale) or a for a in qs]


@register.assignment_tag(takes_context=True)
def has_questions(context, page):
    return Question.objects.live().child_of(page).exists()


@register.assignment_tag(takes_context=True)
def can_vote(context, question):
    request = context['request']
    if hasattr(question, 'freetextquestion'):
        return question.freetextquestion.can_vote(request.user)
    return question.can_vote(request.user)


@register.assignment_tag(takes_context=True)
def user_choice(context, question):
    request = context['request']
    choices = question.get_main_language_page().specific.user_choice(
        request.user)
    if choices.all().count() == 1:
        return choices.first().title
    else:
        choice_titles = [c.title for c in choices.all()]

        return ", ".join(choice_titles)
