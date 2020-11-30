#!/bin/bash
. /Users/angeloporretta/eb-virt/bin/activate
cd /Users/angeloporretta/django_project

for i in 1 2 3 4 5
do
  python manage.py pull_twitter_data "election" --batchsize=500
  python manage.py pull_twitter_data "us politics" --batchsize=500
  python manage.py pull_twitter_data "uk politics" --batchsize=500
  python manage.py pull_twitter_data "canadian politics" --batchsize=1500
  python manage.py pull_twitter_data "covid" --batchsize=100
  python manage.py process_twitter_data --batchsize=1000
  # Process the stats
  python manage.py process_sentiment_pie_stats "election"
  python manage.py process_sentiment_pie_stats "covid"
  python manage.py process_sentiment_pie_stats "uk politics"
  python manage.py process_sentiment_pie_stats "us politics"
  python manage.py process_sentiment_pie_stats "canadian politics"
done