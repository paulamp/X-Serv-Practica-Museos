# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0006_remove_comentario_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=30)),
                ('size', models.CharField(max_length=20)),
                ('background', models.CharField(max_length=30)),
                ('titulo', models.CharField(max_length=50)),
            ],
        ),
    ]
