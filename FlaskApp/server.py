import json
from elasticsearch import Elasticsearch
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token="790035594604867584-Jhmohj3Dk2z5LotbHwzm9LFFLFgfUjc"
access_token_secret="XVXmduRvXAr3z3BSXfEPQzwyisrbwAcIuktCLYWcywjM2"
consumer_key="XlLab1tBNL1NAws6FwAjL8r3i"
consumer_secret="bzcuCYinbhJ63KfbD7e7I8pdE9ZWCvRx58X2Dm7cFCQFeTPFZP"

es=Elasticsearch("https://search-newtweetmapcloud-cqcpw6xnfeq2dnscys2soadpe4.us-west-2.es.amazonaws.com")
class StdOutListener(StreamListener):
    
    def on_data(self, doc_data):
        print doc_data
        json_data=json.loads(doc_data)
        try:
            data={}
            if json_data['coordinates'] is not None:
                data["lat"]=json_data['coordinates']['coordinates'][0]
                data["longtitude"]=longtitude=json_data['coordinates']['coordinates'][1]
            elif json_data['place'] is not None:
                data["lat"]=json_data['place']['bounding_box']['coordinates'][0][0][0]
                data["longtitude"]=json_data['place']['bounding_box']['coordinates'][0][0][1]
            else:
                return
            data["text"]=json_data['text']
            data["name"]=json_data['user']['name']
            data["created_at"]=json_data['created_at']
            print data
            res=es.index(index="cloud", doc_type='tweet', body=data)
            print res['created']
        except:
            return 

    def on_error(self, status):
        print status

if __name__ == "__main__":
    while True:
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            stream.filter(track=['car', 'house', 'country'])

        except:
            continue