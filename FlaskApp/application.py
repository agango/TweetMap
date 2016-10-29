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

es=Elasticsearch()
    
app=Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html', context=js_value)


newlocations=[]
@app.route("/search", methods=["GET", "POST"])
def searchtweet():
    lat=request.form['lat']
    lng=request.form['lng'];
    #queries all tweets within 20 km of the point on the map the user clicked on
    newRes=es.search(index="newtweetcloudfinal", body={
        "query":{
            "filtered":{
                 "filter":{
                    "geo_distance" : {
                        "distance" : "20km", 
                        "location" : {
                            "lat" : lat, 
                            "lon" : lng
                        }
                    }
                }
            }
        }
    })
    counter=0
    for val in newRes['hits']['hits']:
        counter+=1
        newlocations.append({'latlng':{'lat':val["_source"]["location"]["lon"], 'lng':val["_source"]["location"]["lat"]}, 'text':val["_source"]["text"], 'name':val["_source"]["name"]})
    return jsonify(results=newlocations)

@app.route("/search/<searchword>",methods=["GET"])
def search(searchword):
    newRes=es.search(index="newtweetcloudfinal", body={
        "query":
            {"match":
                {"_all":
                    searchword
                }
            },
        "size": 1000
    })
    counter=0
    for val in newRes['hits']['hits']:
        counter+=1
        newlocations.append({'latlng':{'lat':val["_source"]["location"]["lon"], 'lng':val["_source"]["location"]["lat"]}, 'text':val["_source"]["text"], 'name':val["_source"]["name"]})
    return jsonify(results=newlocations)

if __name__ == "__main__":
    app.run(debug=True)








