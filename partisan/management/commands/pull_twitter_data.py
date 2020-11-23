from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.retrievers.twitter import twitter_retriever

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('hashtag', type=str, help='The hashtag you want to search and collect data for.')
        parser.add_argument('--batchsize', type=int, help='The amount of records you want to import. NOTE: Depending on found records, actual ammount pulled in could be less.', default=10, required=False)

    def handle(self, *args, **kwargs):
        tw_retriever = twitter_retriever()
        msg = tw_retriever.searchTweets(kwargs['hashtag'], kwargs['batchsize'])
        self.stdout.write(self.style.SUCCESS(msg))