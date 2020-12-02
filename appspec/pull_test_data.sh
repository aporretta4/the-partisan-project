#!/bin/bash
ENVDIR="/home/ec2-user/venv/"
if [ ! -d "$ENVDIR" ]; then
  python3 -m venv /home/ec2-user/venv
fi
. /home/ec2-user/venv/bin/activate
cd /var/app/current

for i in 1 2 3 4 5
do
  python3 manage.py pull_twitter_data "election" --batchsize=100
  python3 manage.py pull_twitter_data "us politics" --batchsize=100
  python3 manage.py pull_twitter_data "uk politics" --batchsize=100
  python3 manage.py pull_twitter_data "canadian politics" --batchsize=1500
  python3 manage.py pull_twitter_data "covid" --batchsize=100
  python3 manage.py process_twitter_data --batchsize=2000
  # Process the stats
  python3 manage.py process_sentiment_pie_stats "election"
  python3 manage.py process_sentiment_pie_stats "covid"
  python3 manage.py process_sentiment_pie_stats "uk politics"
  python3 manage.py process_sentiment_pie_stats "us politics"
  python3 manage.py process_sentiment_pie_stats "canadian politics"
done