# Generated by Django 3.1 on 2021-02-13 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0026_merge_20210122_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='historical_sentiment_stat',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('neutral_sentiment_average', models.DecimalField(decimal_places=5, max_digits=6, null=True)),
                ('mixed_sentiment_average', models.DecimalField(decimal_places=5, max_digits=6, null=True)),
                ('positive_sentiment_average', models.DecimalField(decimal_places=5, max_digits=6, null=True)),
                ('negative_sentiment_average', models.DecimalField(decimal_places=5, max_digits=6, null=True)),
                ('processed_records_count', models.BigIntegerField(null=True)),
                ('data_source', models.CharField(choices=[('re', 'Reddit'), ('tw', 'Twitter'), ('nt', 'New York Times')], max_length=2)),
                ('month_dt', models.DateTimeField(editable=False)),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='statistic_for', to='partisan.search_term')),
            ],
        ),
    ]