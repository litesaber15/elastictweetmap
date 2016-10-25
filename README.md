# elastictweetmap
A scalable tweet map using AWS Elastic Beanstalk and Elasticsearch

Components: 
- Tweet stream: Stream tweets with geo-location in push-message fashion using [Tweepy](http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html).
- [AWS Elasticsearch](https://aws.amazon.com/elasticsearch-service/?sc_channel=PS&sc_campaign=elasticsearch_2015&sc_publisher=google&sc_medium=elasticsearch_service_b&sc_content=elasticsearch_p&sc_detail=aws%20elastic%20search&sc_category=elasticsearch&sc_segment=96544045594&sc_matchtype=p&sc_country=US): Persistent storage and index for tweets.
- Amazon SQS: Message queuing service that alerts webapp when a new tweet has been found. 
- Back-end: Fetches tweets in realtime as well as those stored persistently and displays them onto the front-end. 
- Front-end: Maps API. 
- AWS Elastic Beanstalk: For load balancing.

AWS Elasticsearch instance: [URL]('https://search-es-twitter-yarekxa5djp3rkj7kp735gvacy.us-west-2.es.amazonaws.com/')

[Elasticsearch Python API](https://elasticsearch-py.readthedocs.io/en/master/) is used to connect with the instance. Use the [Sense plugin](https://chrome.google.com/webstore/detail/sense-beta/lhjgkmllcaadmopgmanpapmpjgmfcfig?hl=en) to query the Elasticsearch instance for debug. [Link to JSON tutorial](http://joelabrahamsson.com/elasticsearch-101/) for querying Elasticsearch.

The following are skimmed from the twitter stream and inserted into elastic search:
- id
- text
- timestamp
- coordinates
- place

Example of JSON object stored in Elasticsearch as well as the message body of SQS notification:
```json
	{
	   "id": 787531772296769500,
	   "text": "I truly have the best family!! I love that you guys took the time… https://t.co/DjArPPiHdf",
	   "time": "1476597180805",
	   "coordinates": {
	      "type": "Point",
	      "coordinates": [
	         -117.87728023,
	         34.1181941
	      ]
	   },
	   "place": {
	      "country": "United States",
	      "bounding_box": {
	         "type": "Polygon",
	         "coordinates": [
	            [
	               [
	                  -117.890263,
	                  34.10549
	               ],
	               [
	                  -117.890263,
	                  34.165551
	               ],
	               [
	                  -117.809111,
	                  34.165551
	               ],
	               [
	                  -117.809111,
	                  34.10549
	               ]
	            ]
	         ]
	      },
	      "country_code": "US",
	      "attributes": {},
	      "place_type": "city",
	      "url": "https://api.twitter.com/1.1/geo/id/eb1bb64775708bc1.json",
	      "full_name": "Glendora, CA",
	      "id": "eb1bb64775708bc1",
	      "name": "Glendora"
	   }
    }
```

Python packages needed for installation (pip install packagename):
- tweepy
- elasticsearch
- boto
