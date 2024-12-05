from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "OMNIA is live and pulling insights from the zeitgeist!"})

@app.route('/get-twitter-trends', methods=['GET'])
def get_twitter_trends():
    return jsonify({"message": "Twitter trends fetched successfully"})

import os
import tweepy
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "OMNIA is live and pulling insights from the zeitgeist!",
        "routes": {
            "/get-twitter-trends": "Fetches Twitter trends"
        }
    })

@app.route('/get-twitter-trends', methods=['GET'])
def get_twitter_trends():
    try:
        client = tweepy.Client(bearer_token=os.getenv('TWITTER_API_KEY'))
        trends = client.get_trends_place(1)  # 1 is the WOEID for worldwide
        return jsonify({"trends": trends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
