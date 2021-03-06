# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-26 03:48
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(0, 'Unknown'), (10, 'Customer'), (20, 'Lecturer'), (30, 'Counselor'), (40, 'Admin')], default=0)),
                ('approved', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'None'), (1, 'Account'), (2, 'Customer'), (3, 'Admin'), (8, 'Customer Details'), (9, 'Message')], default=0)),
                ('timePerformed', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions_account', to='loan.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Master', 'Master'), ('Degree', 'Degree'), ('Diploma', 'Diploma'), ('Certificate', 'Certificate'), ('Other', 'Other')], max_length=15)),
                ('course', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=700)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_account', to='loan.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=50)),
                ('postalcode', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('country', models.CharField(default='KENYA', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=300)),
                ('body', models.CharField(max_length=1000)),
                ('sender_deleted', models.BooleanField(default=False)),
                ('target_deleted', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sender', to='loan.Account')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_target', to='loan.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('read', models.BooleanField(default=False)),
                ('sent_timestamp', models.DateTimeField(auto_now_add=True)),
                ('read_timestamp', models.DateTimeField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_account', to='loan.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='loan.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=50)),
                ('lastname', models.CharField(blank=True, max_length=50)),
                ('IDNO', models.CharField(blank=True, max_length=50)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('birthday', models.DateField(default=datetime.date(1900, 1, 1))),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles_company', to='loan.Organization')),
                ('primaryCompany', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles_primarycompany', to='loan.Account')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='loan.Profile'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
