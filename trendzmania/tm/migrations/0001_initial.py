# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import tm.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=75, verbose_name='User name', validators=[tm.models.validate_not_spaces])),
                ('email', models.EmailField(db_index=True, unique=True, max_length=75, verbose_name='email adress', validators=[tm.models.validate_not_spaces])),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name', validators=[tm.models.validate_not_spaces])),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('phone', models.IntegerField(verbose_name='Telephone')),
                ('address1', models.CharField(max_length=60, verbose_name='Address1')),
                ('address2', models.CharField(max_length=60, verbose_name='Address2')),
                ('city', models.CharField(max_length=40, verbose_name='City')),
                ('country', models.CharField(max_length=40, verbose_name='Country')),
                ('state', models.CharField(max_length=40, verbose_name='State')),
                ('zipcode', models.CharField(max_length=40, verbose_name='Postal code')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active')),
                ('activation_key', models.CharField(max_length=40, verbose_name='activation key', blank=True)),
            ],
            options={
                'db_table': 'user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
    ]
