from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

from src.generate_directions import generate

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.get('/api')
def action():
    source = 'Copperas Cove'
    destination = 'Dallas'
    response = generate(source, destination)

    return response

if __name__ == '__main__':
    app.run(debug=True, port=3000)