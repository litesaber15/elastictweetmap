import tweepy  
import sys  
import json
from textwrap import TextWrapper  
from datetime import datetime  
import boto.sqs
from boto.sqs.message import Message
#credentials.py should be placed along with this file
from credentials import consumer_key, consumer_secret, access_token, access_token_secret, es_host, sqs_name, aws_region, aws_id, aws_key

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

class StreamListener(tweepy.StreamListener):  
  status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

  def __init__(self, sqs, sqs_name):
    super(StreamListener, self).__init__()
    self.sqs = sqs
    self.sqs_queue = self.sqs.get_queue(sqs_name)
    self.count = 1
    self.limit = 1000
    #filter by language to reduce possibility of non-ascii text
    self.supportedLang = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ar']

  def on_status(self, status):
    try:
      json_data = status._json

      #do some processing if tweet is of supported language and has geo-location
      if json_data['coordinates'] is not None and json_data['lang'] in self.supportedLang:
        print('Tweet #'+str(self.count) + ' @'+json_data['user']['screen_name'])
        print(json_data['text'].lower().encode('ascii','ignore').decode('ascii'))
        
        #create JSON object of relevant content from response
        skimmed = {
                    'id': json_data['id'],
                    'time': json_data['timestamp_ms'],
                    'text': json_data['text'].lower().encode('ascii','ignore').decode('ascii'),
                    'coordinates': json_data['coordinates'],
                    'place': json_data['place'],
                    'handle': json_data['user']['screen_name']
                  }

        #add notification of new tweet to SQS
        self.sqs.send_message(self.sqs_queue, skimmed)
        print('SQS Notif created')

        self.count += 1
        if self.count > self.limit:
          print('Disconnecting...')
          streamer.disconnect()

    except Exception as e:
      print(e)
      pass #CAREFUL when debugging: This will not terminiate on an exception


#connect with SQS
try:
  sqs = boto.sqs.connect_to_region(aws_region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
except Exception as e:
  print('Could not connect to SQS')
  print(e)
print('Connected to AWS SQS: '+ str(sqs))

#initialize streamer
streamer = tweepy.Stream(auth=auth, listener=StreamListener(sqs, sqs_name), timeout=30000)
#filter for these terms in tweet text
terms = [ 
        'trump', 'usa', 'wanderlust'
        ,'movies','sports','music','finance','technology'
        ,'fashion','science','travel','health','cricket'
        ,'india', 'love', 'shit','bjp', 'aap', 'india'
        ,'epl', 'football','goal', '1-0']
#stream
streamer.filter(track=terms)