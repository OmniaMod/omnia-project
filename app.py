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
        auth = tweepy.OAuth1UserHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET'),
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_SECRET')
        )
        api = tweepy.API(auth)
        trends_result = api.get_place_trends(1)
        trends_data = [
            {"name": trend["name"], "url": trend["url"]}
            for trend in trends_result[0]["trends"]
        ]
        return jsonify({"trends": trends_data})
    except Exception as e:
        print(f"Error fetching trends: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
