# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, validators=[django.core.validators.RegexValidator(b'^(?:\\w+?-\\w+?)|virtual$')])),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='EuscanResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('result', models.TextField(blank=True)),
                ('scan_time', models.FloatField(null=True, blank=True)),
                ('ebuild', models.CharField(max_length=256, blank=True)),
            ],
            options={
                'get_latest_by': 'datetime',
            },
        ),
        migrations.CreateModel(
            name='Herd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('herd', models.CharField(unique=True, max_length=128, validators=[django.core.validators.RegexValidator(b'^\\S+?$')])),
                ('email', models.CharField(blank=True, max_length=128, null=True, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('n_packages_gentoo', models.IntegerField(default=0)),
                ('n_packages_overlay', models.IntegerField(default=0)),
                ('n_packages_outdated', models.IntegerField(default=0)),
                ('n_versions_gentoo', models.IntegerField(default=0)),
                ('n_versions_overlay', models.IntegerField(default=0)),
                ('n_versions_upstream', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Maintainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('email', models.CharField(unique=True, max_length=128, validators=[django.core.validators.EmailValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Overlay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, validators=[django.core.validators.RegexValidator(b'^\\S+?$')])),
                ('description', models.TextField(null=True, blank=True)),
                ('homepage', models.TextField(null=True, blank=True)),
                ('overlay_path', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(b'^(?:\\w+?-\\w+?)|virtual$')])),
                ('name', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(b'^\\S+?$')])),
                ('description', models.TextField(blank=True)),
                ('homepage', models.TextField(blank=True)),
                ('n_versions', models.IntegerField(default=0)),
                ('n_packaged', models.IntegerField(default=0)),
                ('n_overlay', models.IntegerField(default=0)),
                ('herds', models.ManyToManyField(to='djeuscan.Herd', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=128)),
                ('message', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(to='djeuscan.Package')),
            ],
        ),
        migrations.CreateModel(
            name='RefreshPackageQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField(default=0)),
                ('package', models.ForeignKey(to='djeuscan.Package')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot', models.CharField(default=b'', max_length=128, blank=True)),
                ('revision', models.CharField(max_length=128)),
                ('version', models.CharField(max_length=128)),
                ('packaged', models.BooleanField()),
                ('overlay', models.CharField(default=b'gentoo', max_length=128, db_index=True, blank=True, validators=[django.core.validators.RegexValidator(b'^\\S+?$')])),
                ('urls', models.TextField(blank=True)),
                ('vtype', models.CharField(max_length=128, blank=True)),
                ('handler', models.CharField(db_index=True, max_length=128, blank=True)),
                ('confidence', models.IntegerField(default=0)),
                ('ebuild_path', models.CharField(max_length=256, blank=True)),
                ('metadata_path', models.CharField(max_length=256, null=True, blank=True)),
                ('stabilization_candidate', models.DateField(default=None, null=True, db_index=True, blank=True)),
                ('package', models.ForeignKey(to='djeuscan.Package')),
            ],
        ),
        migrations.CreateModel(
            name='VersionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('slot', models.CharField(default=b'', max_length=128, blank=True)),
                ('revision', models.CharField(max_length=128)),
                ('version', models.CharField(max_length=128)),
                ('packaged', models.BooleanField()),
                ('overlay', models.CharField(default=b'gentoo', max_length=128, blank=True, validators=[django.core.validators.RegexValidator(b'^\\S+?$')])),
                ('action', models.IntegerField(choices=[(1, b'Added'), (2, b'Removed')])),
                ('vtype', models.CharField(max_length=128, blank=True)),
                ('package', models.ForeignKey(to='djeuscan.Package')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryLog',
            fields=[
                ('log_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djeuscan.Log')),
                ('category', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(b'^(?:\\w+?-\\w+?)|virtual$')])),
            ],
            bases=('djeuscan.log',),
        ),
        migrations.CreateModel(
            name='HerdLog',
            fields=[
                ('log_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djeuscan.Log')),
            ],
            bases=('djeuscan.log',),
        ),
        migrations.CreateModel(
            name='MaintainerLog',
            fields=[
                ('log_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djeuscan.Log')),
                ('maintainer', models.ForeignKey(to='djeuscan.Maintainer')),
            ],
            bases=('djeuscan.log',),
        ),
        migrations.CreateModel(
            name='WorldLog',
            fields=[
                ('log_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djeuscan.Log')),
            ],
            bases=('djeuscan.log',),
        ),
        migrations.AddField(
            model_name='problemreport',
            name='version',
            field=models.ForeignKey(blank=True, to='djeuscan.Version', null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='last_version_gentoo',
            field=models.ForeignKey(related_name='last_version_gentoo', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='djeuscan.Version', null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='last_version_overlay',
            field=models.ForeignKey(related_name='last_version_overlay', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='djeuscan.Version', null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='last_version_upstream',
            field=models.ForeignKey(related_name='last_version_upstream', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='djeuscan.Version', null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='maintainers',
            field=models.ManyToManyField(to='djeuscan.Maintainer', blank=True),
        ),
        migrations.AddField(
            model_name='herd',
            name='maintainers',
            field=models.ManyToManyField(to='djeuscan.Maintainer'),
        ),
        migrations.AddField(
            model_name='euscanresult',
            name='package',
            field=models.ForeignKey(to='djeuscan.Package'),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('package', 'revision', 'version', 'overlay')]),
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together=set([('category', 'name')]),
        ),
        migrations.AddField(
            model_name='herdlog',
            name='herd',
            field=models.ForeignKey(to='djeuscan.Herd'),
        ),
    ]
