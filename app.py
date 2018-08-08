from flask import Flask, request
from mapper import display, route
from graph import graph_to_json
from io import BytesIO
import random

app = Flask(__name__)
root = "http://storage.googleapis.com/hotrod-kelda/graphs/"

@app.route('/map/location', methods=['GET'])
def location():
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    z = float(request.args.get('z'))
    w = float(request.args.get('w'))

    g = display(x, y, z, w)
    return graph_to_json(g)

@app.route('/map/route', methods=['GET'])
def find_route():
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    z = float(request.args.get('z'))
    w = float(request.args.get('w'))

    g = route(x, y, z, w)
    return graph_to_json(g)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)
