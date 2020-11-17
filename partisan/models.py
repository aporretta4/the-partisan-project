from django.db import models
from random import randrange

class search_term(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term = models.CharField(editable=False,unique=False,max_length=255)

class tweet(models.Model):
    id = models.BigIntegerField(primary_key=True,editable=False,unique=True)
    text = models.CharField(max_length=2048, )
    text_hash = models.CharField(max_length=128,null=True,unique=True)
    author_id = models.BigIntegerField(editable=False)
    created_at = models.DateTimeField(default='1970-01-01 00:00:00+00:00')
    pie_stat_processed = models.BooleanField(default=False)
    nlp_processed = models.BooleanField(default=False)
    nlp_neutral_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_positive_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_negative_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_mixed_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    term = models.ForeignKey(search_term,null=False,on_delete=models.RESTRICT)

    @staticmethod
    def searchTermTweets(searched_term: str):
        term = search_term.objects.filter(term=searched_term)
        if term.count() != 0:
            return tweet.objects.filter(term_id=term[0].id).all()
        else:
            return []

    @staticmethod
    def getSentimentTweet(searched_term: str, sentiment: str):
        term = search_term.objects.filter(term=searched_term)
        if term.count() != 0:
            if sentiment == 'positive':
                positive_tweet= tweet.objects.filter(term_id=term[0].id, nlp_positive_sentiment__gt=0.95)
                return positive_tweet[randrange(positive_tweet.count())].text
            elif sentiment == 'negative':
                negative_tweet = tweet.objects.filter(term_id=term[0].id, nlp_negative_sentiment__gt=0.95)
                return negative_tweet[randrange(negative_tweet.count())].text
            elif sentiment == 'neutral':
                neutral_tweet = tweet.objects.filter(term_id=term[0].id, nlp_neutral_sentiment__gt=0.95)
                return neutral_tweet[randrange(neutral_tweet.count())].text
            else:
                return ''
        else:
            return ''

class tw_retriever_metadata(models.Model):
    id = models.CharField(primary_key=True,editable=False,unique=True,max_length=255)
    val = models.TextField(blank=False,null=False)

class pie_chart_sentiment_stat(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term = models.OneToOneField(search_term,null=False,on_delete=models.RESTRICT,related_name='statistic_of')
    neutral_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    mixed_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    positive_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    negative_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    processed_records_count = models.BigIntegerField(editable=True,null=True)
