from credentials import aws_key, aws_id, aws_region, sqs_name
from time import sleep
import json
import boto.sqs
from boto.sqs.message import Message
import ast
from alchemyapi import AlchemyAPI

class NotificationManager():
	def __init__(self, aws_id, aws_key, aws_region='us-west-2', sqs_name='new-tweet-notifs'):
		try:
			#connect with sqs
			self.sqs = boto.sqs.connect_to_region(aws_region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
			self.sqs_queue = self.sqs.get_queue(sqs_name)
			self.alc = AlchemyAPI()
		except Exception as e:
			print('Could not connect to SQS')
			print(e)
		print('Connected to AWS SQS: '+ str(self.sqs))

	def openNotifications(self):
		while True:
			#poll for new notifs every second
			rs = self.sqs_queue.get_messages() #result set
			
			if len(rs) > 0:
				for m in rs:
					print('Opening notification')
					body = m.get_body()
					tweet= ast.literal_eval(body)
					#do something with the tweet
					print(tweet['text'])
					response = self.alc.sentiment("text", tweet['text'])
					if(response['status']=='ERROR'):
						print('ERROR')
						break
					tweet['type'] = response["docSentiment"]["type"]
					print("Sentiment: "+ tweet['type'])

					#send processed tweet to SNS


					#delete notification when done
					self.sqs_queue.delete_message(m)
					print('Done')
			else:
				sleep(1)
			

#do the magic
notman = NotificationManager(aws_id, aws_key)
notman.openNotifications()