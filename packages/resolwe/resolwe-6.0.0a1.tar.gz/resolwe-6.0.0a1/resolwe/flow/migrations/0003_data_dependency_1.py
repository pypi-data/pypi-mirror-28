# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-21 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0002_set_process_owners'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=[
            migrations.CreateModel(
                name='DataDependency',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ],
                options={
                    'db_table': 'flow_data_parents',
                },
            ),
            migrations.AlterField(
                model_name='data',
                name='parents',
                field=models.ManyToManyField(related_name='children', through='flow.DataDependency', to='flow.Data'),
            ),
            migrations.AddField(
                model_name='datadependency',
                name='child',
                field=models.ForeignKey(db_column='from_data_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='flow.Data'),
            ),
            migrations.AddField(
                model_name='datadependency',
                name='parent',
                field=models.ForeignKey(db_column='to_data_id', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='flow.Data'),
            ),
        ])
    ]
