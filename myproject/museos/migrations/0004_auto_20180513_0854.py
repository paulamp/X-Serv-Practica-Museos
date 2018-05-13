# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos', '0003_museo_descripcion_entidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.CharField(default=b'', max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='museo',
            name='numComentario',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='museo',
            name='barrio',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='museo',
            name='descripcion',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='museo',
            name='descripcion_entidad',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='museo',
            name='direccion',
            field=models.CharField(default=b'', max_length=250),
        ),
        migrations.AlterField(
            model_name='museo',
            name='distrito',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='museo',
            name='email',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='museo',
            name='horario',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='museo',
            name='localidad',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='museo',
            name='nombre',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='museo',
            name='provincia',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='museo',
            name='telefono',
            field=models.CharField(default=b'', max_length=25),
        ),
        migrations.AlterField(
            model_name='museo',
            name='transporte',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='ubicacion',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='museo',
            name='url',
            field=models.CharField(default=b'', max_length=250),
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
