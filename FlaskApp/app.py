import json
import requests
import pandas
from elasticsearch import Elasticsearch
from flask import Flask, render_template
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token="790035594604867584-Jhmohj3Dk2z5LotbHwzm9LFFLFgfUjc"
access_token_secret="XVXmduRvXAr3z3BSXfEPQzwyisrbwAcIuktCLYWcywjM2"
consumer_key="XlLab1tBNL1NAws6FwAjL8r3i"
consumer_secret="bzcuCYinbhJ63KfbD7e7I8pdE9ZWCvRx58X2Dm7cFCQFeTPFZP"
uri="search-tweetmapcloud-sx3dvn7cnmdzc3ncz7w2zw7w6m.us-west-2.es.amazonaws.com"

def data():
	es=Elasticsearch()
	res=es.search(index)

class StdOutListener(StreamListener):

    def on_data(self, doc_data):
    	print doc_data
        #query=json.dumps(doc_data)
        #response=requests.post(uri, data=query)
        #print response

    def on_error(self, status):
        print status

app=Flask(__name__)

@app.route("/")
def main():
	
	return render_template('index.html')

if __name__ == "__main__":
	app.run()
	while True:
		try:
			l = StdOutListener()
			auth = OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_token, access_token_secret)
			stream = Stream(auth, l)
			stream.filter(track=['the'])

		except AttributeError:
			continue