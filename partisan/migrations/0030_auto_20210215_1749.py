# Generated by Django 3.1 on 2021-02-16 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0029_auto_20210212_2055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historical_sentiment_stat',
            old_name='mixed_sentiment_average',
            new_name='mixed_sentiment_aggregate',
        ),
        migrations.RenameField(
            model_name='historical_sentiment_stat',
            old_name='negative_sentiment_average',
            new_name='negative_sentiment_aggregate',
        ),
        migrations.RenameField(
            model_name='historical_sentiment_stat',
            old_name='neutral_sentiment_average',
            new_name='neutral_sentiment_aggregate',
        ),
        migrations.RenameField(
            model_name='historical_sentiment_stat',
            old_name='positive_sentiment_average',
            new_name='positive_sentiment_aggregate',
        ),
    ]
