from django import forms
from models import Choice
from django.utils.translation import ugettext_lazy as _


class TextVoteForm(forms.Form):
    answer = forms.CharField(required=True)


class NumericalTextVoteForm(forms.Form):
    answer = forms.RegexField(
        "^[0-9]+$", required=True, error_messages={
            'invalid':
                "You did not enter a numerical value. Please try again."})


class VoteForm(forms.Form):
    choice = forms.MultipleChoiceField(
        required=True,
        error_messages={'required': _("You didn't select a choice")})

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = [(
            c.pk, c.title) for c in Choice.objects.all()]
