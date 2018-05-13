# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0004_auto_20180513_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='contenido',
            field=models.CharField(default=b'', max_length=400),
        ),
    ]
