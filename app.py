from flask import Flask, request, jsonify
#import sqlite3

import os
from search.mlScrap import getData

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Init app
app = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome("/opt/render/project/.render/chrome/opt/google/chrome/chrome", chrome_options=chrome_options)
driver.maximize_window()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Api para scrappear ML</h1>"



# Flask maps HTTP requests to Python functions.
# The process of mapping URLs to functions is called routing.
@app.route('/data', methods=['GET'])
def data():
    query = request.args.get('search')
    print(query)
    return getData(query, chrome)
    
# A method that runs the application server.
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=False, threaded=True, port=5000)