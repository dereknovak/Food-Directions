from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import json
import requests
import os

from src.search import search_restaurants
from src.agents import ask_agent

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.get('/api')
def action():
    return 'Hello world'

@app.post('/api/ask')
def ask():
    data = json.loads(request.data)
    print()
    src = data['source']
    dest = data['destination']
    context = data['context']

    route = f'Route from {src} to {dest}.'
    
    return ask_agent(route, context)


if __name__ == '__main__':
    app.run(debug=True, port=3000)