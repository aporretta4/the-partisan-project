# Generated by Django 3.1 on 2020-10-30 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0007_auto_20201029_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='nlp_mixed_sentiment',
            field=models.DecimalField(decimal_places=20, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='nlp_negative_sentiment',
            field=models.DecimalField(decimal_places=20, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='nlp_positive_sentiment',
            field=models.DecimalField(decimal_places=20, max_digits=30, null=True),
        ),
    ]