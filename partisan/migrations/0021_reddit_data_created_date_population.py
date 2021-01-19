from partisan.models import reddit_comment
from time import timezone
import django.core.validators
import praw
from django.db import migrations, models
from django_project.settings import REDDIT_APP_SECRET
from datetime import datetime, timezone
from time import sleep


def retrieve_submission_created_dates(apps, schema_editor):
  reddit_submission = apps.get_model('partisan', 'reddit_submission')
  reddit_interactor = praw.Reddit(
    client_id="s1hHWMH_ekUzrQ",
    client_secret=REDDIT_APP_SECRET,
    redirect_uri="http://127.0.0.1:8000",
    user_agent="PartisanProject"
  )
  reddit_interactor.read_only = True
  submissions = reddit_submission.objects.filter(created_at__range=['1969-12-31', '1971-01-02'])
  i = 0
  for submission in submissions:
    reddit_sub = reddit_interactor.submission(id=submission.submission_id)
    dt = datetime.fromtimestamp(reddit_sub.created_utc)
    submission.created_at = str(dt.replace(tzinfo=timezone.utc))
    submission.save()
    sleep(0.1)
    i = i + 1
    print('Processed ' + str(i) + ' out of ' + str(len(submissions)) + ' Reddit submissions. Percentage: %' + str(100*(i / len(submissions))))

def reverse_submission_created_dates(apps, schema_editor):
  reddit_submission = apps.get_model('partisan', 'reddit_submission')
  submissions = reddit_submission.objects.all()
  for submission in submissions:
    submission.created_at = '1970-01-01 00:00:00+00:00'
    submission.save()

def retrieve_comment_created_dates(apps, schema_editor):
  reddit_comments = apps.get_model('partisan', 'reddit_comment')
  reddit_interactor = praw.Reddit(
    client_id="s1hHWMH_ekUzrQ",
    client_secret=REDDIT_APP_SECRET,
    redirect_uri="http://127.0.0.1:8000",
    user_agent="PartisanProject"
  )
  reddit_interactor.read_only = True
  comments = reddit_comments.objects.filter(created_at__range=['1969-12-31', '1971-01-02'])
  i = 0
  for comment in comments:
    reddit_comment = reddit_interactor.comment(id=comment.comment_id)
    dt = datetime.fromtimestamp(reddit_comment.created_utc)
    comment.created_at = str(dt.replace(tzinfo=timezone.utc))
    comment.save()
    sleep(0.1)
    i = i + 1
    print('Processed ' + str(i) + ' out of ' + str(len(comments)) + ' Reddit comments. Percentage: %' + str(100 * (i / len(comments))))

def reverse_comment_created_dates(apps, schema_editor):
  reddit_comment = apps.get_model('partisan', 'reddit_comment')
  comments = reddit_comment.objects.all()
  for comment in comments:
    comment.created_at = '1970-01-01 00:00:00+00:00'
    comment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('partisan', '0020_auto_20210119_0713'),
    ]

    operations = [
      migrations.RunPython(retrieve_comment_created_dates, reverse_comment_created_dates),
      migrations.RunPython(retrieve_submission_created_dates, reverse_submission_created_dates)
    ]
