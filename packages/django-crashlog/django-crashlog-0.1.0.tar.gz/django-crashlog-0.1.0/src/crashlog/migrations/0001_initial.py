# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('class_name', models.CharField(max_length=128, verbose_name='type')),
                ('message', models.TextField()),
                ('traceback', models.TextField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('server_name', models.CharField(db_index=True, max_length=128)),
                ('username', models.CharField(blank=True, db_index=True, null=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
