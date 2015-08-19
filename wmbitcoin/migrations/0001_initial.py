# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wmposts', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wmcomment', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('recipient', models.ForeignKey(related_name='comment_received_by', to=settings.AUTH_USER_MODEL)),
                ('related_comment', models.ForeignKey(related_name='linked_comment', to='wmcomment.BaseComment')),
                ('sender', models.ForeignKey(related_name='comment_sent_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NestedCommentTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('recipient', models.ForeignKey(related_name='nested_comment_received_by', to=settings.AUTH_USER_MODEL)),
                ('related_nested_comment', models.ForeignKey(related_name='nested_comment', to='wmcomment.NestedComment')),
                ('sender', models.ForeignKey(related_name='nested_comment_sent_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('recipient', models.ForeignKey(related_name='received_by', to=settings.AUTH_USER_MODEL)),
                ('related_post', models.ForeignKey(related_name='linked_post', to='wmposts.BasePost')),
                ('sender', models.ForeignKey(related_name='sent_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tid', models.CharField(default=b'', unique=True, max_length=36)),
                ('amount', models.FloatField()),
                ('status', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=64)),
                ('date_withdrawn', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
            ],
        ),
    ]
