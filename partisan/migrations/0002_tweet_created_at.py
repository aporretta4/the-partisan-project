# Generated by Django 3.1 on 2020-09-13 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(default='1970-01-01T00:00:00+00:00'),
        ),
    ]