# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('djeuscan', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_upstream_info', models.BooleanField(default=True)),
                ('feed_portage_info', models.BooleanField(default=False)),
                ('feed_show_adds', models.BooleanField(default=True)),
                ('feed_show_removals', models.BooleanField(default=True)),
                ('feed_ignore_pre', models.BooleanField(default=False)),
                ('feed_ignore_pre_if_stable', models.BooleanField(default=False)),
                ('email_activated', models.BooleanField(default=True)),
                ('email_every', models.IntegerField(default=1, choices=[(1, b'On updates'), (2, b'Weekly'), (3, b'Monthly')])),
                ('email_ignore_pre', models.BooleanField(default=False)),
                ('email_ignore_pre_if_stable', models.BooleanField(default=False)),
                ('last_email', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(to='djeuscan.Category')),
                ('herds', models.ManyToManyField(to='djeuscan.Herd')),
                ('maintainers', models.ManyToManyField(to='djeuscan.Maintainer')),
                ('overlays', models.ManyToManyField(to='djeuscan.Overlay')),
                ('packages', models.ManyToManyField(to='djeuscan.Package')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
