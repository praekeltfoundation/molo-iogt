# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_polls_index(apps, schema_editor):
    from molo.core.models import Main
    from molo.polls.models import PollsIndexPage
    main = Main.objects.all().first()

    if main:
        polls_index = PollsIndexPage(title='Polls', slug='polls')
        main.add_child(instance=polls_index)
        polls_index.save_revision().publish()


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_pollsindexpage'),
    ]

    operations = [
        migrations.RunPython(create_polls_index),
    ]
