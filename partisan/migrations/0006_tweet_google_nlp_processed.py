# Generated by Django 3.1 on 2020-10-26 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0005_auto_20201026_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='google_nlp_processed',
            field=models.BooleanField(default=False),
        ),
    ]