import tweepy
import json

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key="L2edGlDjo2FUxRSUL1S2mh8gY"
consumer_secret="rTdVnUGJ6FP0Czr67vj9ELwr3m1kml2Bg26orTRodu60URBj5O"
access_token="789927305804218368-E8Uj5Ct5H5BMYrEGEFTHu6uNZFFxdls"
access_token_secret="AZtW0krPGCoQs4OwGsKMRSmpGTeej3iBev3vvqL6B9MdC"

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
	def on_status(self, status):
		json_data = status._json
		if json_data['coordinates']:
			skimmed = {
            	        'id': json_data['id'],
                	    'time': json_data['timestamp_ms'],
                    	'text': json_data['text'].lower().encode('ascii','ignore').decode('ascii'),
                    	'coordinates': json_data['coordinates'],
                    	'place': json_data['place']
                  	}
			print(skimmed)
		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':
	l = StdOutListener()
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = tweepy.Stream(auth, l)
	#filter for these terms in tweet text
	terms = [
		'programming' , 'elections', 'Trump', 'usa', 'wanderlust'
		,'movies','sports','music','finance','technology'
		,'fashion','science','travel','health','cricket'
		,'india', 'love', 'shit','bjp', 'aap', 'india'
		,'epl', 'football','goal', '1-0' ]
	#stream
	#stream.filter(None,terms)
	stream.filter(track=terms)
