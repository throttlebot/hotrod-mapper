from flask import Flask, send_file
from graph import *
from io import BytesIO
import random

app = Flask(__name__)
root = "http://storage.googleapis.com/hotrod-kelda/graphs/"

@app.route('/')
def server_map():
    g = download_json_graph(root + "graph-{}.json".format(random.randint(0, 99)))
    color_shortest(g)
    buf = BytesIO()
    save_to_buf(g, buf)
    return send_file(buf, mimetype="image/png")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
