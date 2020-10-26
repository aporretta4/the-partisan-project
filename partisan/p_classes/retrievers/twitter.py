import json
import logging
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from urllib.parse import quote_plus
from django_project.settings import TW_BEARER_TOKEN
from partisan.models import tweet, tw_retriever_metadata

class twitter_retriever:
    TWITTER_SEARCH_ENDPOINT = 'https://api.twitter.com/1.1/search/tweets.json'
    def __init__(self):
        super().__init__()

    def searchTweets(self, query: str, count: int = 100, tag: str=''):
        resp = {}
        processed_count = 0
        request_string = self.TWITTER_SEARCH_ENDPOINT + '?count=' + str(count) + '&tweet_mode=extended'
        tw_meta = tw_retriever_metadata.objects.filter(id='tw_last_id')
        last_id = '0'
        if tw_meta:
            request_string += '&since_id=' + tw_meta[0].val
            last_id = tw_meta[0].val
        try:
            resp = requests.get(request_string + '&q=' + quote_plus(query), headers={'Authorization': 'Bearer ' + TW_BEARER_TOKEN})
            if resp.status_code == 200:
                for result in resp.json()['statuses']:
                    dt = datetime.strptime(result['created_at'], '%a %b %d %H:%M:%S %z %Y')
                    last_id = result['id']
                    if 'retweeted_status' in result:
                        tw = tweet(id=result['id'],text=result['retweeted_status']['full_text'],author_id=result['user']['id'],created_at=dt.__str__())
                        tw.save()
                        processed_count += 1
                self.__iterateMetadata(last_id=last_id)
            else:
                resp.raise_for_status()
        except HTTPError as ex:
            logging.error('Error status code: ' + str(resp.status_code) + ' when querying Twitter api from twitter_retriever: ' + str(ex))
        except Exception as ex:
            logging.error(str(ex))
        finally:
            self.__iterateMetadata(last_id=last_id)
            return 'Successfully processed ' + str(processed_count) + ' tweets.'

    def __iterateMetadata(self, last_id: str):
        tw_meta_last = tw_retriever_metadata(id="tw_last_id",val=last_id)
        tw_meta_last.save()
        tw_meta_throttle = tw_retriever_metadata(id="tw_throttle",val=datetime.now().strftime('%Y-%m-%d %H:%M:%S%z'))
        tw_meta_throttle.save()
