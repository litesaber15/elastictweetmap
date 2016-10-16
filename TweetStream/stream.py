import tweepy  
import sys  
import json  
from textwrap import TextWrapper  
from datetime import datetime  
from elasticsearch import Elasticsearch
from credentials import consumer_key, consumer_secret, access_token, access_token_secret, es_host

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)

es = Elasticsearch(es_host)

class StreamListener(tweepy.StreamListener):  
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            #print 'n%s %s' % (status.author.screen_name, status.created_at)

            json_data = status._json
            #print json_data['text']

            es.create(index="tweets",
                      doc_type="twitter_twp",
                      body=json_data
                     )

        except Exception as e:
            print(e)
            pass

streamer = tweepy.Stream(auth=auth, listener=StreamListener(), timeout=30000)

#keywords to filter for
terms = ['love','trump']

streamer.filter(None,terms)