from elasticsearch import Elasticsearch
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token="790035594604867584-Jhmohj3Dk2z5LotbHwzm9LFFLFgfUjc"
access_token_secret="XVXmduRvXAr3z3BSXfEPQzwyisrbwAcIuktCLYWcywjM2"
consumer_key="XlLab1tBNL1NAws6FwAjL8r3i"
consumer_secret="bzcuCYinbhJ63KfbD7e7I8pdE9ZWCvRx58X2Dm7cFCQFeTPFZP"
es=Elasticsearch("https://search-tweetmapcloud-sx3dvn7cnmdzc3ncz7w2zw7w6m.us-west-2.es.amazonaws.com")

class StdOutListener(StreamListener):
    def on_data(self, doc_data):
        try:
            res=es.index(index="cloud", doc_type='tweet', body=doc_data)
            print res['created']
        except ValueError:
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
            stream.filter(track=['trump'], locations=[-180, -90, 180, 90])

        except AttributeError:
            continue