from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.retrievers.twitter import twitter_retriever

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('hashtag', type=str, help='The hashtag you want to search and collect data for.')

    def handle(self, *args, **kwargs):
        tw_retriever = twitter_retriever()
        msg = tw_retriever.searchTweets(kwargs['hashtag'], 100)
        self.stdout.write(self.style.SUCCESS(msg))