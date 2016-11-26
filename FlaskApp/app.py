import json
from flask import request
from elasticsearch import Elasticsearch
from flask import Flask, render_template, jsonify



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
    application.run(debug=True, port=8080)








