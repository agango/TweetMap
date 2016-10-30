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
mapping='''
    {"mappings":{
        "tweet":{
            "properties":{
                "location":{
                    "type":"geo_point"
                },
                "name":{
                    "type":"string"
                },
                "text":{
                    "type":"string"
                }
            }
        }
    }     
}'''
es=Elasticsearch([{'host':"search-newtweetmap-5jvth6g6xzg4zohqr2oxc33gda.us-west-2.es.amazonaws.com", 'port':80, 'use_ssl':False}])
es.indices.create(index='newfinaltweetmap', body=mapping)
class StdOutListener(StreamListener):
    
    def on_data(self, doc_data):
        json_data=json.loads(doc_data)
        try:
            data={}
            data["location"]={}
            if json_data['coordinates'] is not None:
                data["location"]["lat"]=json_data['coordinates']['coordinates'][1]
                data["location"]["lon"]=json_data['coordinates']['coordinates'][0]
            elif json_data['place'] is not None:
                data["location"]["lat"]=json_data['place']['bounding_box']['coordinates'][0][0][1]
                data["location"]["lon"]=json_data['place']['bounding_box']['coordinates'][0][0][0]
            else:
                return
            data["name"]=json_data['user']['name']
            data["text"]=json_data['text']
            res=es.index(index="newfinaltweetmap", doc_type='tweet', body=data)
            print (res['created'])
        except:
            print(traceback.print_exc())
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
