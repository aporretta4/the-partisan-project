from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0030_auto_20210215_1749'),
    ]

    operations = [
        migrations.RunSQL(
            'UPDATE partisan_reddit_submission SET historical_stat_processed = 1 WHERE text IS NULL;',
            'UPDATE partisan_reddit_submission SET historical_stat_processed = 0 WHERE text IS NULL;'
        )
    ]
