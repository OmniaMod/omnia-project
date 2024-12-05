import os
import tweepy
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get-twitter-trends', methods=['GET'])
def get_twitter_trends():
    try:
        # Authenticate using v1.1 API credentials
        auth = tweepy.OAuth1UserHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET'),
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_SECRET')
        )
        api = tweepy.API(auth)
        
        # Fetch trends for a specific location (WOEID = 1 for Worldwide)
        trends = api.trends_place(1)
        return jsonify({"trends": trends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
