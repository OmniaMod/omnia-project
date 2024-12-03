
import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "OMNIA is live!"})

if __name__ == '__main__':
    app.run(debug=True)
