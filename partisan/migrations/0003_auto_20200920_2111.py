# Generated by Django 3.1 on 2020-09-21 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0002_tweet_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='tw_retriever_metadata',
            fields=[
                ('id', models.CharField(editable=False, max_length=512, primary_key=True, serialize=False, unique=True)),
                ('val', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(default='1970-01-01 00:00:00+00:00'),
        ),
    ]
