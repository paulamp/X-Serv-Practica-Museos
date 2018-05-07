# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0002_auto_20180503_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='descripcion_entidad',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
