# Generated by Django 3.1 on 2021-01-19 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0019_auto_20201222_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='reddit_comment',
            name='created_at',
            field=models.DateTimeField(default='1970-01-01 00:00:00+00:00'),
        ),
        migrations.AddField(
            model_name='reddit_submission',
            name='created_at',
            field=models.DateTimeField(default='1970-01-01 00:00:00+00:00'),
        ),
    ]
