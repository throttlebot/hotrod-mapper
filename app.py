from flask import Flask, Response, request
from graph import graph_to_json
from shortest_path import download
import random


app = Flask(__name__)

@app.route('/map/location', methods=['GET'])
def location():
    r = random.randint(0, 400)

    g = download(r)

    resp = Response(graph_to_json(g))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)
