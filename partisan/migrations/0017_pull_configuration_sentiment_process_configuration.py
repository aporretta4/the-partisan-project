# Generated by Django 3.1 on 2020-12-21 17:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0016_auto_20201215_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='pull_configuration',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('term_name', models.CharField(max_length=255, unique=True)),
                ('data_source', models.CharField(choices=[('re', 'Reddit'), ('tw', 'Twitter')], default='re', max_length=2)),
                ('items_per_run', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)])),
            ],
        ),
        migrations.CreateModel(
            name='sentiment_process_configuration',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('data_source', models.CharField(choices=[('re', 'Reddit'), ('tw', 'Twitter')], default='re', max_length=2)),
                ('items_per_run', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)])),
                ('term', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pull_config_of', to='partisan.search_term')),
            ],
        ),
    ]