import json
from elasticsearch import Elasticsearch
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boto3
from watson_developer_cloud import AlchemyLanguageV1
import time

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

tweets = []

es=Elasticsearch([{'host':"search-tweet-3jeiq36jepy2fixj7nbot6kzci.us-east-1.es.amazonaws.com", 'port':80, 'use_ssl':False}])
# es.indices.create(index='newfinaltweetmap', body=mapping)
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

            tweets.append(data)
            if(len(tweets)>6):
                return False
            print("added")
            print(data)

        except:
            print(traceback.print_exc())
            return 

    def on_error(self, status):
        print(status)





# def addto_elastic(data):
#     res=es.index(index="newfinaltweetmap", doc_type='tweet', body=data)
#     print (res['created'])


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='tweetmapSQS')
sns = boto3.client('sns')

def addto_queue(data):


    js_value = json.dumps(data)
    response = queue.send_message(MessageBody=js_value)
    # response = queue.send_message(MessageBody='boto3',MessageAttributes=data)
    print("added to queue")


alchemy_language = AlchemyLanguageV1(api_key='b144cdedbb632e744d1acdaa34198f7c3fb42a75')

def process_message():
    for message in queue.receive_messages(MessageAttributeNames=['name']):
        lis = json.loads(format(message.body))
        for tweet in lis:

            print(tweet)
            # print('{0}'.format(message.body))

            response = json.dumps(alchemy_language.sentiment(
                text=tweet['text']),
              indent=2)
            print(response)
            tweet['response'] = response
            print(type(tweet))
            sns.publish(TopicArn = 'arn:aws:sns:us-east-1:990257065467:tweetsns', Message = json.dumps({'default':json.dumps(tweet)}),MessageStructure='json')
            # addto_elastic(tweet)
        message.delete()



if __name__ == "__main__":
    while True:
        try:
            
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            stream.filter(languages=["en"],track=['car', 'house', 'country'])
            print("about to add tweets to SQS que")
            addto_queue(tweets)
            print("about to process")
            process_message()
            time.sleep(10)
        except:
            continue


