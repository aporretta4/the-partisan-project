# Generated by Django 3.1 on 2021-01-21 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0022_auto_20210121_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentiment_process_configuration',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pull_config_of', to='partisan.search_term'),
        ),
    ]
