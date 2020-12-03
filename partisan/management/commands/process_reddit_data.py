from django.core.management.base import BaseCommand
from partisan.models import reddit_comment, reddit_submission
from partisan.p_classes.nlp.sentimentable import sentimentable

class Command(BaseCommand):

  def add_arguments(self, parser):
    parser.add_argument('--commentbatchsize', type=int, help='The amount of records you want to run through AWS comprehend.', default=100, required=False)
    parser.add_argument('--submissionbatchsize', type=int, help='The amount of records you want to run through AWS comprehend.', default=100, required=False)

  def handle(self, *args, **kwargs):
    reddit_comments = reddit_comment.objects.filter(nlp_processed=False).order_by('id')[:kwargs['commentbatchsize']]
    sentimentable.saveTextSentiment(sentimentable_classes=reddit_comments)
    reddit_submissions = reddit_submission.objects.filter(nlp_processed=False).exclude(text='').order_by('id')[:kwargs['submissionbatchsize']]
    sentimentable.saveTextSentiment(sentimentable_classes=reddit_submissions)
