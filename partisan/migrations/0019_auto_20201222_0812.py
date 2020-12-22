from django.db import migrations

def determine_sentiment_source(apps, schema_editor):
    sentiment_stats = apps.get_model('partisan', 'pie_chart_sentiment_stat').objects.all()
    for sentiment_stat in sentiment_stats:
        if sentiment_stat.term.term[0:2] == 'r/':
            sentiment_stat.data_source = 're'
        else:
            sentiment_stat.data_source = 'tw'
        sentiment_stat.save()

def revert(apps, schema_editor):
    return

class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0018_auto_20201222_0811'),
    ]

    operations = [
        migrations.RunPython(determine_sentiment_source, revert),
    ]
