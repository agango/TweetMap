import json
from elasticsearch import Elasticsearch
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boto3
from watson_developer_cloud import AlchemyLanguageV1

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
            
            print("before queue")
            addto_queue(data)
            
            # addto_elastic(body)

            process_message()
            print("after process")

        except:
            print(traceback.print_exc())
            return 

    def on_error(self, status):
        print(status)





def addto_elastic(data):
    res=es.index(index="newfinaltweetmap", doc_type='tweet', body=data)
    print (res['created'])


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='tweetmapSQS')

def addto_queue(data):

    js_value = json.dumps(data)
    response = queue.send_message(MessageBody=js_value)
    # response = queue.send_message(MessageBody='boto3',MessageAttributes=data)
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

alchemy_language = AlchemyLanguageV1(api_key='b144cdedbb632e744d1acdaa34198f7c3fb42a75')


def process_message():
    n = 0
    for message in queue.receive_messages(MessageAttributeNames=['name']):
        print(str(n))
        n = n + 1
        # # Get the custom author message attribute if it was set
        # author_text = ''
        # if message.message_attributes is not None:
        #     author_name = message.message_attributes.get('Author').get('StringValue')
        #     if author_name:
        #         author_text = ' ({0})'.format(author_name)

        # # Print out the body and author (if set)
        print('{0}'.format(message.body))


        response = json.dumps(alchemy_language.sentiment(
            text=('{0}'.format(message.body))),
          indent=2)
        print(response)
        # message.delete()



# if __name__ == "__main__":
#     while True:
#         try:
#             # l = StdOutListener()
#             # auth = OAuthHandler(consumer_key, consumer_secret)
#             # auth.set_access_token(access_token, access_token_secret)
#             # stream = Stream(auth, l)
#             # stream.filter(track=['car', 'house', 'country'])
            

#         except:
#             continue
process_message()