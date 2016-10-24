import tweepy
import json
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

#host = "search-jask-tweetmap-hhk4izgywmbpwob2zah4fcdiry.us-west-2.es.amazonaws.com"
host = "search-es-twitter-yarekxa5djp3rkj7kp735gvacy.us-west-2.es.amazonaws.com"
# Authentication details. To  obtain these visit dev.twitter.com
consumer_key="L2edGlDjo2FUxRSUL1S2mh8gY"
consumer_secret="rTdVnUGJ6FP0Czr67vj9ELwr3m1kml2Bg26orTRodu60URBj5O"
access_token="789927305804218368-E8Uj5Ct5H5BMYrEGEFTHu6uNZFFxdls"
access_token_secret="AZtW0krPGCoQs4OwGsKMRSmpGTeej3iBev3vvqL6B9MdC"

#awsauth = AWS4Auth('AKIAJ7HHWCEARYQMB63Q', 'oRVKo5yx0ceUk9SmYLsTkupo84loy2tAM2kO5gNg','us-west-2','es')

awsauth = AWS4Auth('AKIAJBZBEHQYGYRDJCIQ', '0E5N6o/FZ5CWiT+Y5KA7JitpXQ6mB6px2Xc7/Mgj','us-west-2','es')

es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        use_ssl=True,
        http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )

print(es.info())

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_status(self, status):
        json_data = status._json
        user_info = json_data['user']
        if json_data['coordinates']:
            skimmed = {
                    'id': json_data['id'],
                    'time': json_data['timestamp_ms'],
                    'text': json_data['text'].lower().encode('ascii','ignore').decode('ascii'),
                    'coordinates': json_data['coordinates'],
                    'place': json_data['place']
                    }
            try:
                es.index(index='cloud_tweet', doc_type='twitter', body={
                    'content': json_data['text'].lower().encode('ascii','ignore').decode('ascii'),
                    'user': user_info['name'],
                    'user_id': user_info['id'],
                    'coordinates': json_data['coordinates']['coordinates'],
                    })
            except:
                print('ElasticSearch indexing failed')

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
    while True:
        try:
            stream.filter(track=terms)
        except:
            continue

