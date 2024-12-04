from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "OMNIA is live and pulling insights from the zeitgeist!"})

@app.route('/get-twitter-trends', methods=['GET'])
def get_twitter_trends():
    return jsonify({"message": "Twitter trends fetched successfully"})

