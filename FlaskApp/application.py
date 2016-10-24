import json
import requests
from elasticsearch import Elasticsearch
from flask import Flask, render_template, jsonify



mylocation = []
mylocation.append(40.741895)
mylocation.append(-73.989308)

locations = [
        {'latlng':{'lat': mylocation[0], 'lng': mylocation[1]},'tweet':"my tweet" },
        {'latlng':{'lat': mylocation[1], 'lng': mylocation[1]},'tweet':"my tweet"},
        {'latlng':{'lat': mylocation[0], 'lng': 150.371124},'tweet':"my tweet"},
        {'latlng':{'lat': -33.848588, 'lng': 151.209834},'tweet':"my tweet"},

      ]


js_value = json.dumps(locations)

# es=Elasticsearch("https://search-tweetmapcloud-sx3dvn7cnmdzc3ncz7w2zw7w6m.us-west-2.es.amazonaws.com")
# es.indices.refresh(index="cloud")
    
app=Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html', context=js_value)



@app.route("/search/<searchword>",methods=["GET"])
def search(searchword):
    # newRes=es.search(index="cloud", body={"query":{"match":{"_all":searchword}}})
    # for val in newRes['hits']['hits']:
    #     if 'coordinates' in val.keys():
    #         print val['coordinates']
    # return(json.dumps(newRes))
    return jsonify(results=locations)

if __name__ == "__main__":
    app.run(port=8224,debug=True)








