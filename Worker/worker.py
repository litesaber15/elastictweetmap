from credentials import aws_key, aws_id, aws_region, sqs_name, arn
from time import sleep
import json
import boto.sqs
import boto.sns
from boto.sqs.message import Message
import ast
from alchemyapi import AlchemyAPI
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import sys
from concurrent.futures import ThreadPoolExecutor

class NotificationManager():
	def __init__(self, aws_id, aws_key, es, aws_region='us-west-2', sqs_name='new-tweet-notifs'):
		try:
			#connect with sqs
			self.sqs = boto.sqs.connect_to_region(aws_region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
			self.sqs_queue = self.sqs.get_queue(sqs_name)
			self.alc = AlchemyAPI()
			self.sns = boto.sns.connect_to_region(aws_region)
			self.es = es
			self.thread_pool = ThreadPoolExecutor(max_workers=4)
		except Exception as e:
			print('Could not connect')
			print(e)
		print('Connected to AWS SQS: '+ str(self.sqs))

	def worker_task(self, m):
		error = False
		print('Opening notification')
		body = m.get_body()
		tweet= ast.literal_eval(body)
		#do something with the tweet
		print(tweet['text'])
		response = self.alc.sentiment("text", tweet['text'])
		if(response['status']=='ERROR'):
			print('ERROR')
			error = True
		if not error:
			tweet['sentiment'] = response["docSentiment"]["type"]
			print("Sentiment: "+ tweet['sentiment'])

			#add to Elasticsearch
			try:
				self.es.index(index="tweets", doc_type="twitter_twp", body=tweet)
			except Exception as e:
				print('Elasticserch indexing failed')
				print(e)


			json_string = json.dumps(tweet)
			#send processed tweet to SNS
			self.sns.publish(arn, json_string, subject='Sub')

			#delete notification when done
			self.sqs_queue.delete_message(m)
			print('Done')

	def openNotifications(self):
		while True:
			#poll for new notifs every second
			rs = self.sqs_queue.get_messages() #result set
			if len(rs) > 0:
				for m in rs:
					self.thread_pool.submit(self.worker_task, m)

# init Elasticsearch
awsauth = AWS4Auth(aws_id, aws_key,'us-west-2','es')
es = Elasticsearch(
        hosts=[{'host': 'search-es-twitter-yarekxa5djp3rkj7kp735gvacy.us-west-2.es.amazonaws.com', 'port': 443}],
        use_ssl=True,
        http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )

#do the magic
#sys.setdefaultencoding('utf-8')
notman = NotificationManager(aws_id, aws_key, es)
notman.openNotifications()