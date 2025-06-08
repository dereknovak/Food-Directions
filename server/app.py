from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

from src.search import search_restaurants

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.get('/api')
def action():
    return search_restaurants("Closest high-end mexican restaurants from Copperas Cove")

if __name__ == '__main__':
    app.run(debug=True, port=3000)