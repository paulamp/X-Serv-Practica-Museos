# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=500)),
                ('horario', models.CharField(max_length=500)),
                ('transporte', models.CharField(max_length=100)),
                ('accesibilidad', models.IntegerField()),
                ('url', models.CharField(max_length=250)),
                ('direccion', models.CharField(max_length=250)),
                ('localidad', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=50)),
                ('barrio', models.CharField(max_length=50)),
                ('distrito', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('email', models.CharField(max_length=50)),
            ],
        ),
    ]
