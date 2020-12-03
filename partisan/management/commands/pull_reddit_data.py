from re import sub
from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.retrievers.reddit import reddit_retriever

class Command(BaseCommand):

  def add_arguments(self, parser):
    parser.add_argument('subreddit', type=str, help='The subreddit you want to collect data from.')
    parser.add_argument('--submissionbatch', type=int, help='The amount of reddit submissions you want to gather. NOTE: Depending on found records, actual ammount pulled in could be less.', default=10, required=False)
    parser.add_argument('--comments', type=bool, help='Whether or not you want to gather comments as well.', default=False, required=False)
    parser.add_argument('--commentbatch', type=int, help='The amount of reddit comments you want to gather per submission gathered. NOTE: Depending on found records, actual ammount pulled in could be less.', default=10, required=False)

  def handle(self, *args, **kwargs):
    r_retriever = reddit_retriever()
    reddit_submissions = []
    reddit_comments = []
    reddit_submissions = r_retriever.saveRedditSubmissions(
      subreddit_name=kwargs['subreddit'],
      post_count=kwargs['submissionbatch'],
      submission_type='hot'
    )
    if kwargs['comments']:
      for reddit_submission in reddit_submissions:
        reddit_comment_batch = r_retriever.saveRedditComments(
          submission=reddit_submission,
          comment_count=kwargs['commentbatch']
        )
        reddit_comments.append(reddit_comment_batch)
    self.stdout.write(self.style.SUCCESS('Processed ' + str(len(reddit_submissions)) + ' reddit submissions and ' + str(len(reddit_comments)) + ' per reddit comments.'))