import json
from flask import request
from elasticsearch import Elasticsearch
from flask import Flask, render_template, jsonify
import requests



mylocation = []
mylocation.append(40.741895)
mylocation.append(-73.989308)

locations = [
        {'latlng':{'lat': mylocation[0], 'lng': mylocation[1]},'text':"my tweet", 'name':"Abhiroop" },
        {'latlng':{'lat': mylocation[1], 'lng': mylocation[1]},'text':"my tweet", 'name':"Abhiroop"},
        {'latlng':{'lat': mylocation[0], 'lng': 150.371124},'text':"my tweet", 'name':"Abhiroop"},
        {'latlng':{'lat': -33.848588, 'lng': 151.209834},'text':"my tweet", 'name':"Abhiroop", },

      ]

js_value = json.dumps(locations)

es=Elasticsearch([{'host':"search-tweet-3jeiq36jepy2fixj7nbot6kzci.us-east-1.es.amazonaws.com", 'port':80, 'use_ssl':False}])


    
application=Flask(__name__)
@application.route("/")
def main():
    return render_template('index.html', context=js_value)



def addto_elastic(data):
    res=es.index(index="newfinaltweetmap", doc_type='tweet', body=data)
    print (res['created'])



#update frontend here, this function is called when SNS notification comes
#use addto_elastic to add 'msg'/'js' to elasticsearch instance 'es', probably has to reformat data
#msg is tweet data from SNS
def msg_process(msg, tstamp):
    js = json.loads(msg)
    print(js)
    # do stuff here, like calling your favorite SMS gateway API

@application.route('/sns', methods = ['GET', 'POST', 'PUT'])
def sns():
    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)
    except:
        pass

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    print("here")
    print(js)
    print(hdr)
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        r = requests.get(js['SubscribeURL'])
        print("subscribeURL")
        print(r)

    if hdr == 'Notification':
        print("notification")
        msg_process(js['Message'], js['Timestamp'])

    return 'OK\n'


newlocations=[]
@application.route("/search", methods=["GET", "POST"])
def searchtweet():
    lat=request.form['lat']
    lng=request.form['lng'];

    newRes=es.search(index="newfinaltweetmap", body={
        "query":{
            "filtered":{
                 "filter":{
                    "geo_distance" : {
                        "distance" : "1000km", 
                        "location":{
                            "lat" : lat, 
                            "lon" : lng
                        }
                    }
                }
            }
        }, 
        "size":100
    })
    counter=0
    for val in newRes['hits']['hits']:
        counter+=1
        newlocations.append({'latlng':{'lat':val["_source"]["location"]["lat"], 'lng':val["_source"]["location"]["lon"]}, 'text':val["_source"]["text"], 'name':val["_source"]["name"]})
    print(counter)
    return jsonify(results=newlocations)

@application.route("/search/<searchword>",methods=["GET"])
def search(searchword):
    newRes=es.search(index="newfinaltweetmap", body={
        "query":
            {"match":
                {"_all":
                    searchword
                }
            },
            "size":100
    })
    counter=0
    for val in newRes['hits']['hits']:
        counter+=1
        newlocations.append({'latlng':{'lat':val["_source"]["location"]["lat"], 'lng':val["_source"]["location"]["lon"]}, 'text':val["_source"]["text"], 'name':val["_source"]["name"]})
    return jsonify(results=newlocations)

if __name__ == "__main__":
    application.run(host = '129.236.226.219',debug=True, port=80)


