# Generated by Django 3.1 on 2021-01-22 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0023_auto_20210121_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pie_chart_sentiment_stat',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='statistic_of', to='partisan.search_term'),
        ),
    ]
