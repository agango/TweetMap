import json
import requests
import pandas
from elasticsearch import Elasticsearch
from flask import Flask, render_template



mylocation = []
mylocation.append(40.741895)
mylocation.append(-73.989308)
# es=Elasticsearch("https://search-tweetmapcloud-sx3dvn7cnmdzc3ncz7w2zw7w6m.us-west-2.es.amazonaws.com")

# es.indices.refresh(index="cloud")
# newRes=es.search(index="cloud", body={"query":{"match":{"_all":"trump"}}})
# for val in newRes['hits']['hits']:
#     if 'coordinates' in val.keys():
#         print val['coordinates']

locations = [
        {'lat': mylocation[0], 'lng': mylocation[1],'tweet':"my tweet" },
        {'lat': mylocation[1], 'lng': mylocation[1],'tweet':"my tweet"},
        {'lat': mylocation[0], 'lng': 150.371124,'tweet':"my tweet"},
        {'lat': -33.848588, 'lng': 151.209834,'tweet':"my tweet"},
        {'lat': -33.851702, 'lng': 151.216968,'tweet':"my tweet"},
        {'lat': -34.671264, 'lng': 150.863657,'tweet':"my tweet"},
        {'lat': -35.304724, 'lng': 148.662905,'tweet':"my tweet"},
        {'lat': -36.817685, 'lng': 175.699196,'tweet':"my tweet"},
        {'lat': -36.828611, 'lng': 175.790222,'tweet':"my tweet"},
        {'lat': -37.750000, 'lng': 145.116667,'tweet':"my tweet"},
        {'lat': -37.759859, 'lng': 145.128708,'tweet':"my tweet"},
        {'lat': -37.765015, 'lng': 145.133858,'tweet':"my tweet"},

      ]
js_value = json.dumps(locations)
    
app=Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html', context=js_value)

if __name__ == "__main__":
    app.run(debug=True)








