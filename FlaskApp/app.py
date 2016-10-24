import json
import requests
import pandas
from elasticsearch import Elasticsearch
from flask import Flask, render_template



mylocation = []
mylocation.append(40.741895)
mylocation.append(-73.989308)
es=Elasticsearch("https://search-tweetmapcloud-sx3dvn7cnmdzc3ncz7w2zw7w6m.us-west-2.es.amazonaws.com")

es.indices.refresh(index="cloud")
newRes=es.search(index="cloud", body={"query":{"match":{"_all":"trump"}}})
for val in newRes['hits']['hits']:
    if 'coordinates' in val.keys():
        print val['coordinates']
    
app=Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html', context=mylocation)

if __name__ == "__main__":
    app.run(debug=True)




