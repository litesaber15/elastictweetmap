import tweepy  
import sys  
import json
#from HTMLParser import HTMLParser
from textwrap import TextWrapper  
from datetime import datetime  
from elasticsearch import Elasticsearch
#credentials.py should be placed along with this file
from credentials import consumer_key, consumer_secret, access_token, access_token_secret, es_host

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)

class StreamListener(tweepy.StreamListener):  
  status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

  def __init__(self, es_host):
    super().__init__()
    self.es = Elasticsearch(es_host)
    self.count = 1
    self.limit = 1000

  def on_status(self, status):
    try:
      json_data = status._json
      if json_data['coordinates'] is not None:
        print('Tweet #'+str(self.count))
        skimmed = {
                    'id': json_data['id'],
                    'time': json_data['timestamp_ms'],
                    'text': json_data['text'],
                    'coordinates': json_data['coordinates'],
                    'place': json_data['place']
                  }
        self.es.create(index="tweets", doc_type="twitter_twp", body=skimmed)

        self.count += 1

        if self.count > self.limit:
          print('Disconnecting...')
          streamer.disconnect()

    except Exception as e:
      print(e)
      pass

streamer = tweepy.Stream(auth=auth, listener=StreamListener(es_host), timeout=30000)

#Fill with your own Keywords bellow
terms = ['trump', 'usa', 'wanderlust', 'movies','sports','music','finance','technology','fashion','science','travel','health','cricket','india', 'love', 'shit','bjp', 'aap', 'india']

streamer.filter(None,terms)  
#streamer.userstream(None)