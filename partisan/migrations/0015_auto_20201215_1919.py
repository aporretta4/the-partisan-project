# Generated by Django 3.1 on 2020-11-16 14:31

from django.db import migrations
from django.db.models.functions import Length

def shorten_reddit_comments(apps, schema_editor):
    reddit_comment = apps.get_model('partisan', 'reddit_comment')
    long_comments = reddit_comment.objects.annotate(text_length=Length('text')).filter(text_length__gt=4750)
    for long_comment in long_comments:
        long_comment.text = long_comment.text[0:4740] + '...'
        long_comment.save()

def shorten_reddit_submissions(apps, schema_editor):
    reddit_submission = apps.get_model('partisan', 'reddit_submission')
    long_submissions = reddit_submission.objects.annotate(text_length=Length('text')).filter(text_length__gt=4750)
    for long_submission in long_submissions:
        long_submission.text = long_submission.text[0:4740] + '...'
        long_submission.save()

def revert(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0014_reddit_comment_reddit_submission'),
    ]

    operations = [
        migrations.RunPython(shorten_reddit_comments, revert),
        migrations.RunPython(shorten_reddit_submissions, revert)
    ]
