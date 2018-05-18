# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0008_coleccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='coleccion',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
