# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0007_perfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coleccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('museo', models.ForeignKey(to='museos.Museo')),
                ('perfil', models.ForeignKey(to='museos.Perfil')),
            ],
        ),
    ]
