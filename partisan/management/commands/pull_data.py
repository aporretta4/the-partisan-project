from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.retrievers.twitter import twitter_retriever
from partisan.p_classes.retrievers.reddit import reddit_retriever
from partisan.models import pull_configuration

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.__pullTwitterData(twitter_pull_configs=pull_configuration.objects.filter(data_source='tw'))
        self.__pullRedditData(pull_configuration.objects.filter(data_source='re'))

    def __pullTwitterData(self, twitter_pull_configs: pull_configuration):
        counter = 0
        for tw_pull_conf in twitter_pull_configs:
            tw_retriever = twitter_retriever()
            msg = tw_retriever.searchTweets(tw_pull_conf.term_name, tw_pull_conf.items_per_run)
            self.stdout.write(self.style.SUCCESS(msg))
        return counter

    def __pullRedditData(self, reddit_pull_configs: pull_configuration):
        counter = 0
        reddit_submissions = []
        reddit_comments = []
        for re_pull_conf in reddit_pull_configs:
            r_retriever = reddit_retriever()
            reddit_submissions = r_retriever.saveRedditSubmissions(
                subreddit_name=re_pull_conf.term_name,
                post_count=re_pull_conf.items_per_run,
                submission_type='hot'
            )
            for reddit_submission in reddit_submissions:
                reddit_comment_batch = r_retriever.saveRedditComments(submission=reddit_submission, comment_count=re_pull_conf.items_per_run)
                reddit_comments.append(reddit_comment_batch)
        self.stdout.write(self.style.SUCCESS('ATTEMPTED to pull in ' + str(len(reddit_submissions)) + ' reddit submissions and ATTEMPTED to pull in ' + str(len(reddit_comments)) + ' comments per reddit submission.'))
        return counter