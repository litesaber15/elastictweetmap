import tweepy
import sys  
import json  
from textwrap import TextWrapper  
from datetime import datetime  
from elasticsearch import Elasticsearch


consumer_key="  QAwRcbZjqqCSoKrZchnsY8zlp"
consumer_secret="dWJ8s7dRN97EBWh1m2nZphABK85GF0CH3eqSITEerg22x5iEUO"
access_token="  1545989874-iJjOjUWhO3VWhEPuHXQZmtaGO6Hsm4d5EpZ93Ns"
access_token_secret="iBPTuWEGJp352XJkyEN9GizVtov9gDpzMcA725Fpdg5bO"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)

es = Elasticsearch()

class StreamListener(tweepy.StreamListener):  
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            #print 'n%s %s' % (status.author.screen_name, status.created_at)

            json_data = status._json
            #print json_data['text']

            es.create(index="idx_twp",
                      doc_type="twitter_twp",
                      body=json_data
                     )

        except Exception, e:
            print e
            pass

streamer = tweepy.Stream(auth=auth, listener=StreamListener(), timeout=3000000000 )

#Fill with your own Keywords bellow
terms = ['obiee','oracle']

streamer.filter(None,terms)  
#streamer.userstream(None)
