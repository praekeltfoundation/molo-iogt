# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('votes', models.IntegerField(default=0)),
                ('short_name', models.TextField(help_text=b"The short name will replace the title when downloading your results. e.g '10 years old' would be replaced by '10' in the title column.", null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ChoiceVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateField(auto_now_add=True, null=True)),
                ('choice', models.ManyToManyField(to='polls.Choice', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FreeTextVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField(null=True, blank=True)),
                ('submission_date', models.DateField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(related_name='text_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_name', models.TextField(help_text=b"The short name will replace the title when downloading your results. e.g 'How old are you' would be replaced by 'Age' in the title column.", null=True, blank=True)),
                ('extra_style_hints', models.TextField(default=b'', help_text='Styling options that can be applied to this section and all its descendants', null=True, blank=True)),
                ('show_results', models.BooleanField(default=True, help_text='This option allows the users to see the results.')),
                ('randomise_options', models.BooleanField(default=False, help_text='Randomising the options allows the options to be shown in a different order each time the page is displayed.')),
                ('result_as_percentage', models.BooleanField(default=True, help_text='If not checked, the results will be shown as a total instead of a percentage.')),
                ('allow_multiple_choice', models.BooleanField(default=False, help_text='Allows the user to choose more than one option.')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FreeTextQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='polls.Question')),
                ('numerical', models.BooleanField(default=False, help_text='When selected, this question will allow numerical data only')),
            ],
            options={
                'abstract': False,
            },
            bases=('polls.question',),
        ),
        migrations.AddField(
            model_name='choicevote',
            name='question',
            field=models.ForeignKey(to='polls.Question'),
        ),
        migrations.AddField(
            model_name='choicevote',
            name='user',
            field=models.ForeignKey(related_name='choice_votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_votes',
            field=models.ManyToManyField(related_name='choices', to='polls.ChoiceVote', blank=True),
        ),
        migrations.AddField(
            model_name='freetextvote',
            name='question',
            field=models.ForeignKey(to='polls.FreeTextQuestion'),
        ),
    ]
