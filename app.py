from flask import Flask, request, jsonify
#import sqlite3

import os
from search.mlScrap import getData

# Init app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Api para scrappear ML</h1>"



# Flask maps HTTP requests to Python functions.
# The process of mapping URLs to functions is called routing.
@app.route('/data', methods=['GET'])
def data():
    query = request.args.get('search')
    return getData(query)
    
# A method that runs the application server.
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True, threaded=True, port=5000)