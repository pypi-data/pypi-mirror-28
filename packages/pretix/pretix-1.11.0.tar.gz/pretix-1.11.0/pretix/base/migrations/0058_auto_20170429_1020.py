# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0052_team_teaminvite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpermission',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventpermission',
            name='user',
        ),
        migrations.RemoveField(
            model_name='organizerpermission',
            name='organizer',
        ),
        migrations.RemoveField(
            model_name='organizerpermission',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='permitted',
        ),
        migrations.RemoveField(
            model_name='organizer',
            name='permitted',
        ),
        migrations.AlterField(
            model_name='team',
            name='can_change_teams',
            field=models.BooleanField(default=False, verbose_name='Can change teams and permissions'),
        ),
        migrations.AlterField(
            model_name='team',
            name='limit_events',
            field=models.ManyToManyField(blank=True, to='pretixbase.Event', verbose_name='Limit to events'),
        ),
        migrations.DeleteModel(
            name='EventPermission',
        ),
        migrations.DeleteModel(
            name='OrganizerPermission',
        ),
    ]
