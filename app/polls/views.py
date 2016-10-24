from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

host = "search-jask-tweetmap-hhk4izgywmbpwob2zah4fcdiry.us-west-2.es.amazonaws.com"
awsauth = AWS4Auth('AKIAJ7HHWCEARYQMB63Q', 'oRVKo5yx0ceUk9SmYLsTkupo84loy2tAM2kO5gNg','us-west-2','es')
es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        use_ssl=True,
        http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )
print(es.info())


def index(request):
    return render(request, "polls/maps.html")

def map(request):
    if request.method == 'POST':
	term = request.POST.get('select')
        res = es.search(size=5000, index="cloud_tweet", doc_type="twitter", body={
            "query":{
		"match":{"content":term}	
            }})
        coordinate_array = []
        coordinates = res['hits']
        individual_coordinate_sets = coordinates['hits']
        list_of_dicts = [dict() for num in range (len(individual_coordinate_sets))]
        for idx,element in enumerate(list_of_dicts):
            source_value = individual_coordinate_sets[idx]['_source']
            temp_coordinates = source_value['coordinates']
            tweet_info = source_value['user'] + ": " + source_value['content']
            list_of_dicts[idx] = dict(lng=temp_coordinates[0], lat = temp_coordinates[1])
        return render(request, "polls/maps.html", {'plot':list_of_dicts})
    else:
        return render(request, "polls/maps.html", {'plot':[0]})
"""
    if request.method == 'POST':
        print("Reached here")
        with open('data.txt','r') as f :
            for line in f:
                tweet = eval(line)
                if tweet['coordinates']:
                    print(tweet['coordinates'])
                    coordinates.append(tweet['coordinates']['coordinates'])
    print(coordinates)
"""
